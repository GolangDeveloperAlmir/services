"""Admin-protected HTTP endpoints for user-profile CRUD operations."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import AdminDep, AuthServiceDep, require_admin
from app.auth.service import AdministratorInvariantError
from app.db.session import get_session
from app.users.schemas import UserCreate, UserRead, UserUpdate
from app.users.service import UserService


router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(require_admin)],
)

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_user_service(session: SessionDep) -> UserService:
    """Construct the profile service for the current request session."""
    return UserService(session)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


@router.post(
    "",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    responses={409: {"description": "Email already exists"}},
)
async def create_user(
    data: UserCreate,
    request: Request,
    admin: AdminDep,
    service: UserServiceDep,
) -> UserRead:
    """Create a profile, recording the administrator and request source."""
    if admin.user_id is None:
        raise HTTPException(status_code=403, detail="Forbidden")
    user = await service.create(
        data,
        actor_user_id=admin.user_id,
        source_ip=request.client.host if request.client else None,
    )

    return UserRead.model_validate(user)


@router.get(
    "", response_model=list[UserRead], responses={422: {"description": "Invalid pagination"}}
)
async def get_users(
    service: UserServiceDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> list[UserRead]:
    """Return one bounded page of profiles, newest first."""
    users = await service.get_all(offset, limit)
    return [UserRead.model_validate(user) for user in users]


@router.get(
    "/{user_id}",
    response_model=UserRead,
    responses={404: {"description": "User not found"}},
)
async def get_user(user_id: UUID, service: UserServiceDep) -> UserRead:
    """Return a profile by UUID or respond with ``404``."""
    user = await service.get_by_id(user_id)

    return UserRead.model_validate(user)


@router.patch(
    "/{user_id}",
    response_model=UserRead,
    responses={
        404: {"description": "User not found"},
        409: {"description": "Duplicate email or administrator invariant"},
    },
)
async def update_user(
    user_id: UUID,
    data: UserUpdate,
    request: Request,
    service: UserServiceDep,
    admin: AdminDep,
    auth_service: AuthServiceDep,
) -> UserRead:
    """Update profile fields while preserving administrator safety invariants."""
    if admin.user_id is None:
        raise HTTPException(status_code=403, detail="Forbidden")
    invalidate_sessions = False
    if data.is_active is False:
        try:
            invalidate_sessions = await auth_service.ensure_admin_account_can_change(
                user_id,
                admin.user_id,
                "auth.admin.deactivated",
                request.client.host if request.client else None,
            )
        except AdministratorInvariantError as error:
            raise HTTPException(status_code=409, detail=str(error)) from error
    user = await service.update(
        user_id,
        data,
        actor_user_id=admin.user_id,
        source_ip=request.client.host if request.client else None,
    )
    if invalidate_sessions:
        await auth_service.revoke_user_sessions(user_id)

    return UserRead.model_validate(user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"description": "User not found"},
        409: {"description": "Administrator invariant"},
    },
)
async def delete_user(
    user_id: UUID,
    request: Request,
    service: UserServiceDep,
    admin: AdminDep,
    auth_service: AuthServiceDep,
) -> None:
    """Delete a profile unless doing so violates administrator invariants."""
    if admin.user_id is None:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        invalidate_sessions = await auth_service.ensure_admin_account_can_change(
            user_id,
            admin.user_id,
            "auth.admin.account_deleted",
            request.client.host if request.client else None,
        )
    except AdministratorInvariantError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    await service.delete(
        user_id,
        actor_user_id=admin.user_id,
        source_ip=request.client.host if request.client else None,
    )
    if invalidate_sessions:
        await auth_service.revoke_user_sessions(user_id)
