"""Request and response models for authentication and security audit endpoints."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr
from uuid import UUID


class LoginRequest(BaseModel):
    """Credentials submitted to the local administrator login endpoint."""

    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    password: SecretStr = Field(min_length=1, max_length=128)


class TokenResponse(BaseModel):
    """Opaque bearer token and lifetime returned after successful login."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


class AuthenticatedUser(BaseModel):
    """Public identity details for the current administrator session."""

    id: UUID
    email: EmailStr
    roles: list[str]


class PasswordChangeRequest(BaseModel):
    """Current and replacement secrets for password rotation."""

    model_config = ConfigDict(extra="forbid")

    current_password: SecretStr = Field(min_length=1, max_length=128)
    new_password: SecretStr = Field(min_length=1, max_length=128)


class AdminGrantRequest(BaseModel):
    """Reauthentication and initial/rotated credential for an admin grant."""

    model_config = ConfigDict(extra="forbid")

    current_password: SecretStr = Field(min_length=1, max_length=128)
    target_password: SecretStr = Field(min_length=1, max_length=128)


class AdminRevokeRequest(BaseModel):
    """Current administrator password required to revoke another admin."""

    model_config = ConfigDict(extra="forbid")

    current_password: SecretStr = Field(min_length=1, max_length=128)


class SecurityAuditRecord(BaseModel):
    """Public projection of one persisted security event."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    actor_user_id: UUID | None
    target_user_id: UUID | None
    event_type: str
    source_ip: str | None
    occurred_at: datetime
