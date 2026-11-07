"""Liveness and dependency-readiness probes for deployment health checks."""

from fastapi import APIRouter, HTTPException, Request, status
from sqlalchemy import text


router = APIRouter(tags=["health"])


@router.get("/health/live", include_in_schema=False)
async def liveness() -> dict[str, str]:
    """Report process liveness without probing external dependencies."""
    return {"status": "ok"}


@router.get("/health/ready", include_in_schema=False)
async def readiness(request: Request) -> dict[str, str]:
    """Check PostgreSQL and Redis availability or respond with HTTP 503."""
    try:
        async with request.app.state.engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        await request.app.state.redis.ping()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service dependencies are unavailable",
        ) from error
    return {"status": "ready"}
