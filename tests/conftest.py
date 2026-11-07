"""Shared pytest configuration for isolated service tests."""

import os


os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+asyncpg://test:test@127.0.0.1:5432/user_service_test",
)
os.environ.setdefault("REDIS_URL", "redis://:test@127.0.0.1:6379/15")
