"""Persistence queries and mutations for user profiles."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.model import User


class UserRepository:
    """Execute user-profile queries using a request-scoped async session."""

    def __init__(self, session: AsyncSession):
        """Create a repository bound to an existing database session."""
        self.session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        """Return the matching profile, or ``None`` when it does not exist."""
        return await self.session.get(User, user_id)

    async def get_by_email(self, email: str) -> User | None:
        """Return the profile with the exact normalized email address."""
        statement = select(User).where(User.email == email)

        return await self.session.scalar(statement)

    async def get_all(self, offset: int, limit: int) -> list[User]:
        """Return a stable newest-first page of profiles."""
        statement = (
            select(User).order_by(User.created_at.desc(), User.id).offset(offset).limit(limit)
        )

        result = await self.session.scalars(statement)

        return list(result.all())

    def add(self, user: User) -> None:
        """Stage a new profile in the current transaction."""
        self.session.add(user)

    async def delete(self, user: User) -> None:
        """Stage deletion of a profile in the current transaction."""
        await self.session.delete(user)
