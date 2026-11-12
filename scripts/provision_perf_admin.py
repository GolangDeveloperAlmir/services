"""Create a temporary authenticated load-test identity on a local test database."""

import asyncio
import secrets
from urllib.parse import urlsplit

from app.auth.service import AuthService
from app.core.config import settings
from app.db.session import SessionFactory, redis_client


async def provision() -> str:
    """Create the disposable test administrator and return its session token."""
    email = "performance-admin@example.com"
    password = secrets.token_urlsafe(32)
    async with SessionFactory() as session:
        service = AuthService(session, redis_client)
        await service.bootstrap_admin(email, "Performance Test Administrator", password)
        token, _, _ = await service.login(email, password, "127.0.0.1")
    return token


async def provision_and_close() -> str:
    """Provision the load-test session and close the shared Redis client."""
    try:
        return await provision()
    finally:
        await redis_client.aclose()


def main() -> None:
    """Restrict provisioning to local APP_ENV=test databases ending in _test."""
    database_url = urlsplit(settings.database_url)
    redis_url = urlsplit(settings.redis_url)
    database_name = database_url.path.removeprefix("/")
    local_hosts = {"localhost", "127.0.0.1", "::1", "db", "redis"}
    if (
        settings.app_env != "test"
        or not database_name.endswith("_test")
        or database_url.hostname not in local_hosts
        or redis_url.hostname not in local_hosts
    ):
        raise SystemExit(
            "Performance admin provisioning is restricted to local APP_ENV=test and *_test databases."
        )
    print(asyncio.run(provision_and_close()))


if __name__ == "__main__":
    main()
