"""Alembic runtime configuration for synchronous and asynchronous migrations."""

import asyncio

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.core.config import settings
from app.db.base import Base
from app.auth.models import AuthRole, LocalCredential, SecurityAuditEvent, UserRole  # noqa: F401
from app.users.model import User  # noqa: F401


config = context.config

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Render migrations using the configured database URL without a connection."""
    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    """Run pending migrations on an active synchronous SQLAlchemy connection."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Create an async engine and run migrations against the configured database."""
    config.set_main_option(
        "sqlalchemy.url",
        settings.database_url.replace("%", "%%"),
    )

    configuration = config.get_section(config.config_ini_section)
    if configuration is None:
        raise RuntimeError(f"Configuration section {config.config_ini_section!r} was not found")

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run the async migration routine from Alembic's synchronous entry point."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
