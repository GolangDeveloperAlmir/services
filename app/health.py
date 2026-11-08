"""Liveness and bounded readiness probes for application dependencies."""

import asyncio
import logging
from collections.abc import Awaitable, Callable
from pathlib import Path
from secrets import token_hex

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from redis.asyncio import Redis
from redis.exceptions import RedisError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine

from app.core.config import settings


router = APIRouter(tags=["health"])
logger = logging.getLogger(__name__)
HEALTH_CHECK_TIMEOUT_SECONDS = 2
FRONTEND_DIR = Path(__file__).resolve().parents[1] / "frontend" / "public"


@router.get("/health/live", include_in_schema=False)
async def liveness() -> dict[str, str]:
    """Report process liveness without probing external dependencies."""
    return {"status": "ok"}


async def _check_postgresql(engine: AsyncEngine) -> None:
    """Verify PostgreSQL accepts a lightweight read-only query."""
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))


async def _check_redis(redis: Redis) -> None:
    """Verify Redis session/cache data can be written, read, and removed."""
    key = f"user-service:health:{token_hex(16)}"
    value = token_hex(16)
    if not await redis.set(key, value, ex=HEALTH_CHECK_TIMEOUT_SECONDS + 1, nx=True):
        raise RedisError("Redis health-check key could not be written")
    if await redis.get(key) != value:
        raise RedisError("Redis health-check value could not be read")


async def _check_media_catalog() -> None:
    """Verify the configured operator-managed media directory is available."""
    if not settings.media_root.is_dir():
        raise FileNotFoundError("Media catalog directory is unavailable")


async def _check_frontend_assets() -> None:
    """Verify the frontend entry point and compiled assets are present."""
    required_files = (
        FRONTEND_DIR / "index.html",
        FRONTEND_DIR / "assets" / "app.js",
        FRONTEND_DIR / "assets" / "styles.css",
    )
    if any(not path.is_file() for path in required_files):
        raise FileNotFoundError("Frontend assets are unavailable")


async def _probe(
    name: str,
    check: Callable[[], Awaitable[None]],
) -> tuple[str, str]:
    """Run one probe with a deadline and record failures without leaking details."""
    try:
        await asyncio.wait_for(check(), timeout=HEALTH_CHECK_TIMEOUT_SECONDS)
    except (OSError, RedisError, SQLAlchemyError, TimeoutError) as error:
        logger.warning(
            "Readiness component unavailable",
            extra={"health_component": name, "error_type": type(error).__name__},
        )
        return name, "unavailable"
    return name, "ok"


@router.get("/health/ready", include_in_schema=False)
async def readiness(request: Request) -> JSONResponse:
    """Probe critical dependencies and report component status without secrets."""
    probes = await asyncio.gather(
        _probe(
            "postgresql",
            lambda: _check_postgresql(request.app.state.engine),
        ),
        _probe(
            "redis",
            lambda: _check_redis(request.app.state.redis),
        ),
        _probe("media_catalog", _check_media_catalog),
        _probe("frontend", _check_frontend_assets),
    )
    checks = dict(probes)
    ready = all(result == "ok" for result in checks.values())
    return JSONResponse(
        status_code=200 if ready else 503,
        content={
            "status": "ready" if ready else "unavailable",
            "checks": checks,
        },
    )
