"""Unit tests for service-level email uniqueness and database race handling."""

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError

from app.users.exceptions import EmailAlreadyExistsError
from app.users.service import UserService


class UserRepositoryStub:
    """Minimal repository fake returning one preconfigured email match."""

    def __init__(self, existing_user: SimpleNamespace | None) -> None:
        """Store the user returned by subsequent email lookups."""
        self.existing_user = existing_user

    async def get_by_email(self, email: str) -> SimpleNamespace | None:
        """Return the configured matching user for uniqueness checks."""
        return self.existing_user


def build_service(existing_user: SimpleNamespace | None) -> UserService:
    """Create a service wired to an async session mock and repository stub."""
    service = UserService(AsyncMock())
    service.repository = UserRepositoryStub(existing_user)
    return service


def test_create_rejects_an_existing_email() -> None:
    """Reject an email already owned by a different user."""
    service = build_service(SimpleNamespace(id=uuid4()))

    with pytest.raises(EmailAlreadyExistsError):
        asyncio.run(service.ensure_email_available("used@example.test"))


def test_update_allows_the_current_users_email() -> None:
    """Allow an update to retain its current user's normalized email."""
    user_id = uuid4()
    service = build_service(SimpleNamespace(id=user_id))

    asyncio.run(
        service.ensure_email_available(
            "used@example.test",
            exclude_user_id=user_id,
        )
    )


def test_concurrent_email_conflict_becomes_domain_error() -> None:
    """Translate a concurrent unique-index violation into a domain conflict."""
    existing_user = SimpleNamespace(id=uuid4())
    service = build_service(existing_user)
    service.session.commit.side_effect = IntegrityError(
        "INSERT INTO users",
        {},
        Exception("unique constraint"),
    )

    with pytest.raises(EmailAlreadyExistsError):
        asyncio.run(service.commit(email="used@example.test"))

    service.session.rollback.assert_awaited_once()


def test_update_rejects_an_email_owned_by_another_user() -> None:
    """Reject an update email when another user owns the address."""
    service = build_service(SimpleNamespace(id=uuid4()))

    with pytest.raises(EmailAlreadyExistsError):
        asyncio.run(
            service.ensure_email_available(
                "used@example.test",
                exclude_user_id=uuid4(),
            )
        )
