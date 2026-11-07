"""Identity and authorization abstractions used by protected routes."""

from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

from fastapi import Request


@dataclass(frozen=True)
class Principal:
    """Authenticated subject and the permissions granted for one request."""

    subject: str
    scopes: frozenset[str]
    user_id: UUID | None = None


class IdentityProvider(Protocol):
    """Interface for local, OIDC, or trusted-gateway identity adapters."""

    async def authenticate(self, credential: str, request: Request) -> Principal:
        """Validate a credential in request context and return its principal."""
        ...


class AuthorizationPolicy(Protocol):
    """Permission decision interface; implementations must default to deny."""

    def is_allowed(self, principal: Principal, permission: str) -> bool:
        """Decide whether a principal may perform one named operation."""
        ...


class AdminOnlyPolicy:
    """Allow only principals explicitly carrying a user ID and permission."""

    def is_allowed(self, principal: Principal, permission: str) -> bool:
        """Return whether the principal holds the requested permission."""
        return permission in principal.scopes and principal.user_id is not None
