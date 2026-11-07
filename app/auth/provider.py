"""Adapter that authenticates bearer credentials against local sessions."""

from fastapi import Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.interfaces import Principal
from app.auth.service import ADMIN_ROLE, AuthService, LOGIN_SCOPE


class LocalSessionIdentityProvider:
    """Resolve opaque local sessions and reject non-admin identities."""

    def __init__(self, session: AsyncSession, redis: Redis) -> None:
        """Build the identity adapter with request-scoped database and Redis clients."""
        self.auth_service = AuthService(session, redis)

    async def authenticate(self, credential: str, request: Request) -> Principal:
        """Validate a bearer token and return the active administrator principal."""
        user = await self.auth_service.authenticate_admin(credential)
        return Principal(
            subject=user.email,
            scopes=frozenset({LOGIN_SCOPE, f"role:{ADMIN_ROLE}"}),
            user_id=user.id,
        )
