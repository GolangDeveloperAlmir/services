"""Validated request and response models for profile endpoints."""

from datetime import datetime
from typing import Self
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    model_validator,
)


class UserCreate(BaseModel):
    """Fields accepted when creating a profile; credentials are managed separately."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    email: EmailStr

    full_name: str = Field(
        min_length=1,
        max_length=120,
    )


class UserUpdate(BaseModel):
    """Partial profile update that rejects empty payloads and explicit nulls."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    email: EmailStr | None = None

    full_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=120,
    )

    is_active: bool | None = None

    @model_validator(mode="after")
    def validate_patch(self) -> Self:
        """Require at least one explicitly supplied, non-null field."""
        if not self.model_fields_set:
            raise ValueError("At least one field must be provided")

        for field in self.model_fields_set:
            if getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")

        return self


class UserRead(BaseModel):
    """Public profile representation returned by CRUD endpoints."""

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    email: EmailStr
    full_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
