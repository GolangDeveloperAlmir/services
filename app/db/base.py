"""Shared SQLAlchemy declarative base for application persistence models."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base metadata registry consumed by Alembic and model declarations."""
