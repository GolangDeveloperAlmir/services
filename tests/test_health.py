"""HTTP tests for liveness and dependency-readiness probes."""

import asyncio
from contextlib import asynccontextmanager
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

from fastapi.testclient import TestClient
from redis.exceptions import ConnectionError as RedisConnectionError
from sqlalchemy.exc import OperationalError

from app import health
from app.core.config import settings
from app.main import app


def configure_healthy_dependencies(
    monkeypatch,
    tmp_path: Path,
) -> tuple[AsyncMock, SimpleNamespace]:
    """Provide isolated database, Redis, media, and frontend resources."""
    execute = AsyncMock()

    @asynccontextmanager
    async def connect():
        yield SimpleNamespace(execute=execute)

    engine = SimpleNamespace(connect=Mock(side_effect=connect))
    redis = SimpleNamespace(
        set=AsyncMock(return_value=True),
        get=AsyncMock(),
    )
    redis.get.side_effect = lambda _key: redis.set.await_args.args[1]
    monkeypatch.setattr(app.state, "engine", engine, raising=False)
    monkeypatch.setattr(app.state, "redis", redis, raising=False)

    media_root = tmp_path / "media"
    media_root.mkdir()
    monkeypatch.setattr(settings, "media_root", media_root)

    frontend = tmp_path / "frontend"
    assets = frontend / "assets"
    assets.mkdir(parents=True)
    (frontend / "index.html").touch()
    (assets / "app.js").touch()
    (assets / "styles.css").touch()
    monkeypatch.setattr(health, "FRONTEND_DIR", frontend)

    return execute, redis


def test_readiness_reports_all_critical_components(
    monkeypatch,
    tmp_path: Path,
) -> None:
    """Report PostgreSQL, Redis, media, and frontend availability."""
    execute, redis = configure_healthy_dependencies(monkeypatch, tmp_path)
    client = TestClient(app, base_url="https://localhost")

    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "checks": {
            "postgresql": "ok",
            "redis": "ok",
            "media_catalog": "ok",
            "frontend": "ok",
        },
    }
    execute.assert_awaited_once()
    await_args = execute.await_args
    assert await_args is not None
    assert str(await_args.args[0]) == "SELECT 1"
    redis.set.assert_awaited_once()
    redis.get.assert_awaited_once_with(redis.set.await_args.args[0])


def test_readiness_reports_database_failure_without_exposing_error(
    monkeypatch,
    tmp_path: Path,
) -> None:
    """Return 503 for a database failure while hiding backend exception text."""
    execute, redis = configure_healthy_dependencies(monkeypatch, tmp_path)
    execute.side_effect = OperationalError(
        "SELECT 1",
        {},
        RuntimeError("sensitive database details"),
    )
    client = TestClient(app, base_url="https://localhost")

    response = client.get("/health/ready")

    assert response.status_code == 503
    assert response.json()["status"] == "unavailable"
    assert response.json()["checks"]["postgresql"] == "unavailable"
    assert response.json()["checks"]["redis"] == "ok"
    assert "sensitive database details" not in response.text
    redis.set.assert_awaited_once()


def test_readiness_reports_redis_failure(
    monkeypatch,
    tmp_path: Path,
) -> None:
    """Return 503 when the session and rate-limit cache is unavailable."""
    _, redis = configure_healthy_dependencies(monkeypatch, tmp_path)
    redis.set.side_effect = RedisConnectionError("Redis unavailable")
    client = TestClient(app, base_url="https://localhost")

    response = client.get("/health/ready")

    assert response.status_code == 503
    assert response.json()["checks"]["postgresql"] == "ok"
    assert response.json()["checks"]["redis"] == "unavailable"


def test_readiness_reports_missing_media_and_frontend_assets(
    monkeypatch,
    tmp_path: Path,
) -> None:
    """Mark the service unavailable when runtime-served assets are missing."""
    _, _ = configure_healthy_dependencies(monkeypatch, tmp_path)
    settings.media_root.rmdir()
    (health.FRONTEND_DIR / "assets" / "app.js").unlink()
    client = TestClient(app, base_url="https://localhost")

    response = client.get("/health/ready")

    assert response.status_code == 503
    assert response.json()["checks"]["media_catalog"] == "unavailable"
    assert response.json()["checks"]["frontend"] == "unavailable"
    assert response.json()["checks"]["postgresql"] == "ok"
    assert response.json()["checks"]["redis"] == "ok"


def test_readiness_times_out_slow_database_probe(
    monkeypatch,
    tmp_path: Path,
) -> None:
    """Return unavailable when a database readiness query exceeds its deadline."""
    execute, _ = configure_healthy_dependencies(monkeypatch, tmp_path)

    async def wait_forever(_statement) -> None:
        await asyncio.Event().wait()

    execute.side_effect = wait_forever
    monkeypatch.setattr(health, "HEALTH_CHECK_TIMEOUT_SECONDS", 0.01)
    client = TestClient(app, base_url="https://localhost")

    response = client.get("/health/ready")

    assert response.status_code == 503
    assert response.json()["checks"]["postgresql"] == "unavailable"
    assert response.json()["checks"]["redis"] == "ok"


def test_liveness_does_not_depend_on_external_services() -> None:
    """Keep process liveness independent of databases, cache, and assets."""
    client = TestClient(app, base_url="https://localhost")

    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
