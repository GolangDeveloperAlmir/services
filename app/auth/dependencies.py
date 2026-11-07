"""FastAPI dependencies for constructing auth services and requiring admins."""

from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.interfaces import (
    AdminOnlyPolicy,
    AuthorizationPolicy,
    IdentityProvider,
    Principal,
)
from app.auth.provider import LocalSessionIdentityProvider
from app.auth.service import AuthService, AuthenticationFailed
from app.db.session import get_session


bearer_scheme = HTTPBearer(auto_error=False)
CredentialsDep = Annotated[
    HTTPAuthorizationCredentials | None,
    Depends(bearer_scheme),
]
admin_policy: AuthorizationPolicy = AdminOnlyPolicy()
SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_auth_service(request: Request, session: SessionDep) -> AuthService:
    """Build the authentication service from app-scoped Redis and DB session."""
    redis_client: Redis = request.app.state.redis
    return AuthService(session, redis_client)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


def get_identity_provider(
    request: Request,
    session: SessionDep,
) -> IdentityProvider:
    """Build the local identity provider for this request."""
    redis_client: Redis = request.app.state.redis
    return LocalSessionIdentityProvider(session, redis_client)


IdentityProviderDep = Annotated[IdentityProvider, Depends(get_identity_provider)]


async def require_admin(
    request: Request,
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
    provider: IdentityProviderDep,
) -> Principal:
    """Authenticate a bearer token and deny access unless it is an active admin."""
    if credentials is None or credentials.scheme.casefold() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        principal = await provider.authenticate(credentials.credentials, request)
    except AuthenticationFailed as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        ) from error

    if not admin_policy.is_allowed(principal, "users:admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )
    return principal


AdminDep = Annotated[Principal, Depends(require_admin)]
