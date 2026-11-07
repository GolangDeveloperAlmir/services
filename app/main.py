"""FastAPI composition root, request middleware, and domain error mapping."""

import asyncio
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from time import perf_counter

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.auth.router import router as auth_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.core.telemetry import configure_telemetry
from app.db.session import engine, redis_client
from app.health import router as health_router
from app.users.exceptions import (
    EmailAlreadyExistsError,
    UserNotFoundError,
)
from app.users.router import router as users_router


configure_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Verify dependencies at startup and release telemetry/database clients."""
    app.state.redis = redis_client
    app.state.engine = engine
    async with engine.connect() as connection:
        await connection.exec_driver_sql("SELECT 1")
    await redis_client.ping()

    try:
        yield
    finally:
        if telemetry_provider is not None:
            await asyncio.to_thread(telemetry_provider.shutdown)
        await redis_client.aclose()
        await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(health_router)
telemetry_provider = configure_telemetry(app)


@app.middleware("http")
async def log_http_requests(request: Request, call_next):
    """Reject cleartext requests and attach security headers and timing logs."""
    if request.url.scheme != "https":
        return JSONResponse(
            status_code=426,
            content={"detail": "HTTPS is required"},
            headers={"Upgrade": "TLS/1.2"},
        )

    started_at = perf_counter()
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    if request.url.path.startswith("/auth/"):
        response.headers["Cache-Control"] = "no-store"
    logger.info(
        "HTTP request completed",
        extra={
            "http_method": request.method,
            "http_path": request.url.path,
            "http_status_code": response.status_code,
            "duration_ms": round((perf_counter() - started_at) * 1000, 2),
        },
    )
    return response


@app.exception_handler(RequestValidationError)
async def handle_request_validation_error(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Return validation details without reflecting submitted input values."""
    errors = [
        {key: value for key, value in error.items() if key != "input"} for error in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={"detail": jsonable_encoder(errors)},
    )


@app.exception_handler(UserNotFoundError)
async def handle_user_not_found(request: Request, exc: UserNotFoundError):
    """Map a missing profile domain error to a stable 404 response."""
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.exception_handler(EmailAlreadyExistsError)
async def handle_duplicate_email(
    request: Request,
    exc: EmailAlreadyExistsError,
):
    """Map profile email uniqueness conflicts to HTTP 409."""
    return JSONResponse(
        status_code=409,
        content={"detail": "Email already exists"},
    )
