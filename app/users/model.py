"""Backward-compatible import location for the shared user persistence model."""

from app.db.user_model import User

__all__ = ["User"]
