"""HTTP endpoints for local admin login, credential management, and audit."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, Request, Response, status

from app.auth.dependencies import AdminDep, AuthServiceDep, CredentialsDep
from app.auth.schemas import (
    AdminGrantRequest,
    AdminRevokeRequest,
    AuthenticatedUser,
    LoginRequest,
    PasswordChangeRequest,
    SecurityAuditRecord,
    TokenResponse,
)
from app.auth.service import (
    AuthenticationFailed,
    LoginRateLimited,
)


router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    request: Request,
    service: AuthServiceDep,
) -> TokenResponse:
    """Authenticate an administrator and return a short-lived bearer token."""
    client_ip = request.client.host if request.client else "unknown"
    try:
        token, ttl, _user = await service.login(
            str(data.email),
            data.password.get_secret_value(),
            client_ip,
        )
    except LoginRateLimited as error:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts",
            headers={"Retry-After": str(service.rate_limit_window_seconds)},
        ) from error
    except AuthenticationFailed as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) from error

    return TokenResponse(access_token=token, expires_in=ttl)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: Request,
    admin: AdminDep,
    credentials: CredentialsDep,
    service: AuthServiceDep,
) -> Response:
    """Revoke the current bearer token and return an empty success response."""
    if credentials is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    client_ip = request.client.host if request.client else "unknown"
    if admin.user_id is None:
        raise HTTPException(status_code=403, detail="Forbidden")
    await service.logout(credentials.credentials, admin.user_id, client_ip)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/me", response_model=AuthenticatedUser)
async def get_current_identity(admin: AdminDep) -> AuthenticatedUser:
    """Return the identity and role associated with the current session."""
    if admin.user_id is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return AuthenticatedUser(
        id=admin.user_id,
        email=admin.subject,
        roles=["admin"],
    )


@router.post("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    data: PasswordChangeRequest,
    admin: AdminDep,
    service: AuthServiceDep,
) -> Response:
    """Change the current administrator password and invalidate its sessions."""
    try:
        await service.rotate_password(
            email=admin.subject,
            current_password=data.current_password.get_secret_value(),
            new_password=data.new_password.get_secret_value(),
        )
    except AuthenticationFailed as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current credentials are invalid",
            headers={"WWW-Authenticate": "Bearer"},
        ) from error
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/admins/{target_user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def grant_admin(
    target_user_id: UUID,
    data: AdminGrantRequest,
    request: Request,
    admin: AdminDep,
    service: AuthServiceDep,
) -> Response:
    """Assign admin to another user after reauthenticating the actor."""
    try:
        await service.grant_admin(
            actor_email=admin.subject,
            actor_password=data.current_password.get_secret_value(),
            target_user_id=target_user_id,
            target_password=data.target_password.get_secret_value(),
            source_ip=(request.client.host if request.client else "unknown"),
        )
    except AuthenticationFailed as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current credentials are invalid",
            headers={"WWW-Authenticate": "Bearer"},
        ) from error
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/admins/{target_user_id}/revoke",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def revoke_admin(
    target_user_id: UUID,
    data: AdminRevokeRequest,
    request: Request,
    admin: AdminDep,
    service: AuthServiceDep,
) -> Response:
    """Remove another admin role after reauthenticating the actor."""
    try:
        await service.revoke_admin(
            actor_email=admin.subject,
            actor_password=data.current_password.get_secret_value(),
            target_user_id=target_user_id,
            source_ip=request.client.host if request.client else "unknown",
        )
    except AuthenticationFailed as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current credentials are invalid",
            headers={"WWW-Authenticate": "Bearer"},
        ) from error
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/audit", response_model=list[SecurityAuditRecord])
async def read_security_audit(
    admin: AdminDep,
    service: AuthServiceDep,
    limit: Annotated[int, Query(ge=1, le=500)] = 100,
) -> list[SecurityAuditRecord]:
    """Return a bounded newest-first view of security audit events."""
    events = await service.recent_audit_events(limit)
    return [SecurityAuditRecord.model_validate(event) for event in events]
