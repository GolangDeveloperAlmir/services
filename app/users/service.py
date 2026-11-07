"""Business rules for profile CRUD operations."""

from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.exceptions import (
    EmailAlreadyExistsError,
    UserNotFoundError,
)
from app.users.model import User
from app.users.repository import UserRepository
from app.users.schemas import UserCreate, UserUpdate


class UserService:
    """Validate profile operations and coordinate repository transactions."""

    def __init__(self, session: AsyncSession):
        """Create a profile service using the supplied transaction session."""
        self.session = session
        self.repository = UserRepository(session)

    @staticmethod
    def normalize_email(email: str) -> str:
        """Canonicalize email casing for storage and uniqueness checks."""
        return email.casefold()

    async def ensure_email_available(
        self,
        email: str,
        exclude_user_id: UUID | None = None,
    ) -> None:
        """Reject an email already owned by a different profile."""
        existing_user = await self.repository.get_by_email(email)

        if existing_user is not None and existing_user.id != exclude_user_id:
            raise EmailAlreadyExistsError

    async def commit(
        self,
        email: str | None = None,
        exclude_user_id: UUID | None = None,
    ) -> None:
        """Commit changes and translate concurrent email conflicts to a domain error."""
        try:
            await self.session.commit()

        except IntegrityError as e:
            await self.session.rollback()

            if email is not None:
                existing_user = await self.repository.get_by_email(email)

                if existing_user is not None and existing_user.id != exclude_user_id:
                    raise EmailAlreadyExistsError from e

            raise

    async def create(self, data: UserCreate) -> User:
        """Create and persist a profile after checking normalized email uniqueness."""
        email = self.normalize_email(str(data.email))

        await self.ensure_email_available(email)

        user = User(
            email=email,
            full_name=data.full_name,
        )

        self.repository.add(user)

        await self.commit(email=email)
        await self.session.refresh(user)

        return user

    async def get_by_id(self, user_id: UUID) -> User:
        """Fetch one profile or raise ``UserNotFoundError``."""
        user = await self.repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError

        return user

    async def get_all(self, offset: int = 0, limit: int = 100) -> list[User]:
        """Return a bounded page of profiles in repository-defined order."""
        return await self.repository.get_all(offset, limit)

    async def update(self, user_id: UUID, data: UserUpdate) -> User:
        """Apply only supplied profile fields and persist the updated row."""
        user = await self.get_by_id(user_id)

        changes = data.model_dump(exclude_unset=True)

        email = None

        if "email" in changes:
            email = self.normalize_email(str(changes["email"]))

            await self.ensure_email_available(email, exclude_user_id=user.id)

            changes["email"] = email

        for field, value in changes.items():
            setattr(user, field, value)

        await self.commit(email=email, exclude_user_id=user.id)
        await self.session.refresh(user)

        return user

    async def delete(self, user_id: UUID) -> None:
        """Delete an existing profile and commit the transaction."""
        user = await self.get_by_id(user_id)

        await self.repository.delete(user)
        await self.commit()
