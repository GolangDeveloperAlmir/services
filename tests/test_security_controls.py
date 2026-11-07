"""Regression tests for authentication hardening and admin account invariants."""

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient

from app.auth.dependencies import require_admin
from app.auth.interfaces import AdminOnlyPolicy, Principal
from app.auth.security import (
    hash_password,
    ip_rate_limit_key,
    rate_limit_key,
    session_key,
    validate_password,
    verify_password,
)
from app.auth.service import (
    AdministratorInvariantError,
    AuthService,
    LoginRateLimited,
)
from app.core.config import Settings
from app.main import app
from app.users.router import router as users_router


def test_local_auth_uses_argon2id_and_rejects_common_or_invalid_passwords() -> None:
    """Verify Argon2id use and password length/common-password validation."""
    password = "river-cobalt-lantern-94!"
    password_hash = hash_password(password)

    assert password_hash.startswith("$argon2id$")
    assert verify_password(password_hash, password)
    assert not verify_password(password_hash, "incorrect-password")
    for rejected in ("short", " password long enough", "passwordpassword"):
        with pytest.raises(ValueError):
            validate_password(rejected)


def test_session_and_rate_limit_keys_do_not_contain_secrets_or_identity() -> None:
    """Ensure Redis keys derive from inputs without disclosing raw values."""
    token = "opaque-session-token"

    assert token not in session_key(token)
    assert "admin@example.test" not in rate_limit_key("admin@example.test", "127.0.0.1")
    assert "127.0.0.1" not in ip_rate_limit_key("127.0.0.1")


def test_admin_policy_denies_missing_role_and_identity() -> None:
    """Require both the admin scope and a persisted user identity."""
    policy = AdminOnlyPolicy()

    assert not policy.is_allowed(Principal("user", frozenset()), "users:admin")
    assert not policy.is_allowed(
        Principal("user", frozenset({"users:admin"})),
        "users:admin",
    )
    assert policy.is_allowed(
        Principal("admin", frozenset({"users:admin"}), uuid4()),
        "users:admin",
    )


def test_login_rate_limit_stops_before_database_authentication() -> None:
    """Stop a rate-limited login before querying PostgreSQL."""
    redis = AsyncMock()
    redis.eval.return_value = [6, 1]
    session = AsyncMock()
    service = AuthService(session, redis)

    async def verify_limit() -> None:
        """Assert the over-limit attempt raises before credential lookup."""
        with pytest.raises(LoginRateLimited):
            await service.login("admin@example.test", "some-password", "127.0.0.1")

    asyncio.run(verify_limit())
    session.scalar.assert_not_called()


def test_production_settings_require_tls_and_non_loopback_hosts() -> None:
    """Reject production configurations without TLS or explicit remote hosts."""
    valid = {
        "database_url": "postgresql+asyncpg://user:pass@db.example.test/service?ssl=require",
        "redis_url": "rediss://:pass@cache.example.test:6379/0",
        "app_env": "production",
        "allowed_hosts": ["api.example.test"],
    }
    Settings(**valid)

    with pytest.raises(ValueError, match="TLS"):
        Settings(**{**valid, "redis_url": "redis://:pass@cache.example.test:6379/0"})
    with pytest.raises(ValueError, match="loopback"):
        Settings(**{**valid, "allowed_hosts": ["localhost"]})
    with pytest.raises(ValueError, match="DATABASE_URL"):
        Settings(
            **{
                **valid,
                "database_url": "postgresql+asyncpg://user:pass@db.example.test/service",
            }
        )
    with pytest.raises(ValueError, match="explicit"):
        Settings(**{**valid, "allowed_hosts": [" *.example.test"]})


def test_invalid_production_config_does_not_echo_secret_urls() -> None:
    """Avoid disclosing database or Redis passwords in validation errors."""
    secret = "sensitive-password-marker"
    values = {
        "database_url": f"postgresql+asyncpg://user:{secret}@db.example.test/service",
        "redis_url": f"redis://:{secret}@cache.example.test:6379/0",
        "app_env": "production",
        "allowed_hosts": ["api.example.test"],
    }

    with pytest.raises(ValueError) as error:
        Settings(**values)

    assert secret not in str(error.value)


def test_every_user_route_requires_an_admin() -> None:
    """Ensure each profile API route has the shared admin dependency."""
    routes = [route for route in users_router.routes if isinstance(route, APIRoute)]

    assert routes
    assert all(
        any(dependency.call is require_admin for dependency in route.dependant.dependencies)
        for route in routes
    )


def test_http_is_rejected_and_https_responses_include_security_headers() -> None:
    """Require HTTPS and verify baseline transport security response headers."""
    http_client = TestClient(app)
    https_client = TestClient(app, base_url="https://localhost")

    assert http_client.get("/health/live").status_code == 426
    response = https_client.get("/health/live")
    assert response.status_code == 200
    assert response.headers["strict-transport-security"].startswith("max-age=")
    assert response.headers["x-content-type-options"] == "nosniff"


def test_validation_errors_never_reflect_supplied_passwords() -> None:
    """Keep an invalid login password out of the 422 response body."""
    secret = "do-not-echo-" * 20
    app.state.redis = AsyncMock()
    client = TestClient(app, base_url="https://localhost")

    response = client.post(
        "/auth/login",
        json={"email": "admin@example.test", "password": secret},
    )

    assert response.status_code == 422
    assert secret not in response.text


def test_last_admin_cannot_be_deactivated_or_deleted() -> None:
    """Preserve the last active administrator when validating an account change."""
    target_id = uuid4()
    session = AsyncMock()
    session.get.return_value = SimpleNamespace(id=target_id, is_active=True)
    session.scalar.side_effect = [target_id, 1]
    service = AuthService(session, AsyncMock())

    async def verify_invariant() -> None:
        """Assert account mutation is rejected when it removes the final admin."""
        with pytest.raises(
            AdministratorInvariantError,
            match="last active administrator",
        ):
            await service.ensure_admin_account_can_change(
                target_id,
                uuid4(),
                "auth.admin.account_deleted",
            )

    asyncio.run(verify_invariant())
    session.add.assert_not_called()


def test_admin_deactivation_versions_credentials_and_records_source_ip() -> None:
    """Version admin credentials and include source IP in the audit event."""
    target_id = uuid4()
    target = SimpleNamespace(id=target_id, is_active=True)
    credential = SimpleNamespace(session_version=3)
    session = AsyncMock()
    session.add = Mock()
    session.get.side_effect = [target, credential]
    session.scalar.side_effect = [target_id, 2]
    service = AuthService(session, AsyncMock())

    async def apply_change_guard() -> bool:
        """Run the account-change guard with source address audit metadata."""
        return await service.ensure_admin_account_can_change(
            target_id,
            uuid4(),
            "auth.admin.deactivated",
            "127.0.0.1",
        )

    assert asyncio.run(apply_change_guard())
    assert credential.session_version == 4
    event = session.add.call_args.args[0]
    assert event.event_type == "auth.admin.deactivated"
    assert event.source_ip == "127.0.0.1"
