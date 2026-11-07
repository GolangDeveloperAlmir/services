"""Application services for administrator credentials, sessions, and audit."""

import logging
import secrets
from asyncio import to_thread
from uuid import UUID

from redis.asyncio import Redis
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import (
    AuthRole,
    LocalCredential,
    SecurityAuditEvent,
    UserRole,
)
from app.auth.security import (
    PASSWORD_HASHER,
    hash_password,
    ip_rate_limit_key,
    new_session_token,
    password_needs_rehash,
    rate_limit_key,
    session_key,
    validate_password,
    verify_password,
)
from app.core.config import settings
from app.db.user_model import User


logger = logging.getLogger(__name__)
ADMIN_ROLE = "admin"
LOGIN_SCOPE = "users:admin"
DUMMY_PASSWORD_HASH = PASSWORD_HASHER.hash(secrets.token_urlsafe(32))
INCREMENT_WITH_TTL = """
local results = {}
for index, key in ipairs(KEYS) do
    local count = redis.call('INCR', key)
    if count == 1 then
        redis.call('EXPIRE', key, ARGV[1])
    end
    table.insert(results, count)
end
return results
"""
CREATE_SESSION = """
redis.call('SET', KEYS[1], ARGV[1], 'EX', ARGV[2])
redis.call('SADD', KEYS[2], KEYS[1])
redis.call('EXPIRE', KEYS[2], ARGV[2])
return 1
"""
REVOKE_USER_SESSIONS = """
local sessions = redis.call('SMEMBERS', KEYS[1])
for _, session_key in ipairs(sessions) do
    redis.call('DEL', session_key)
end
redis.call('DEL', KEYS[1])
return #sessions
"""


class AuthenticationFailed(Exception):
    """Raised when supplied credentials cannot authenticate an active admin."""


class LoginRateLimited(Exception):
    """Raised when an IP or email/IP login attempt limit has been exceeded."""


class AdministratorInvariantError(Exception):
    """Raised when an admin-account mutation would violate safety invariants."""


class AuthService:
    """Coordinate credential verification, Redis sessions, roles, and audit."""

    def __init__(
        self,
        session: AsyncSession,
        redis: Redis,
    ) -> None:
        """Bind authentication operations to a database session and Redis client."""
        self.session = session
        self.redis = redis

    @property
    def rate_limit_window_seconds(self) -> int:
        """Return the configured window used to calculate login retry delays."""
        return settings.auth_rate_limit_window_seconds

    async def login(
        self,
        email: str,
        password: str,
        client_ip: str,
    ) -> tuple[str, int, User]:
        """Authenticate an active admin, enforce limits, and issue an opaque session."""
        normalized_email = email.casefold()
        limit_key = rate_limit_key(normalized_email, client_ip)
        ip_limit_key = ip_rate_limit_key(client_ip)
        attempt = await self.redis.eval(
            INCREMENT_WITH_TTL,
            2,
            limit_key,
            ip_limit_key,
            settings.auth_rate_limit_window_seconds,
        )
        pair_attempts, ip_attempts = attempt
        if (
            int(pair_attempts) > settings.auth_rate_limit_attempts
            or int(ip_attempts) > settings.auth_ip_rate_limit_attempts
        ):
            raise LoginRateLimited

        user = await self.session.scalar(select(User).where(User.email == normalized_email))
        credential = None
        if user is not None:
            credential = await self.session.get(LocalCredential, user.id)

        valid_password = await to_thread(
            verify_password,
            credential.password_hash if credential else DUMMY_PASSWORD_HASH,
            password,
        )
        is_admin = False
        if user is not None and credential is not None:
            is_admin = (
                await self.session.scalar(
                    select(UserRole.user_id).where(
                        UserRole.user_id == user.id,
                        UserRole.role_name == ADMIN_ROLE,
                    )
                )
                is not None
            )

        if (
            not valid_password
            or user is None
            or credential is None
            or not credential.is_enabled
            or not user.is_active
            or not is_admin
        ):
            raise AuthenticationFailed

        if await to_thread(password_needs_rehash, credential.password_hash):
            credential.password_hash = await to_thread(hash_password, password)

        token = new_session_token()
        ttl = settings.auth_session_ttl_seconds
        token_key = session_key(token)
        session_value = f"{user.id}:{credential.session_version}"
        await self.redis.eval(
            CREATE_SESSION,
            2,
            token_key,
            f"user-service:user-sessions:{user.id}",
            session_value,
            ttl,
        )
        await self.redis.delete(limit_key)
        self.session.add(
            SecurityAuditEvent(
                actor_user_id=user.id,
                target_user_id=user.id,
                event_type="auth.login.succeeded",
                source_ip=client_ip,
            )
        )
        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            await self.redis.delete(token_key)
            await self.redis.srem(f"user-service:user-sessions:{user.id}", token_key)
            raise
        return token, ttl, user

    async def authenticate_admin(self, token: str) -> User:
        """Resolve a Redis session and recheck account, credential, and admin state."""
        session_value = await self.redis.get(session_key(token))
        if session_value is None:
            raise AuthenticationFailed

        try:
            user_id_text, version_text = session_value.rsplit(":", 1)
            user_id = UUID(user_id_text)
            session_version = int(version_text)
        except (ValueError, AttributeError) as error:
            logger.error("Invalid user ID found in server-side session")
            await self.redis.delete(session_key(token))
            raise AuthenticationFailed from error

        user = await self.session.get(User, user_id)
        credential = await self.session.get(LocalCredential, user_id)
        if user is None or not user.is_active:
            await self.redis.delete(session_key(token))
            raise AuthenticationFailed
        if (
            credential is None
            or not credential.is_enabled
            or credential.session_version != session_version
        ):
            await self.redis.delete(session_key(token))
            raise AuthenticationFailed

        has_admin_role = await self.session.scalar(
            select(UserRole.user_id).where(
                UserRole.user_id == user_id,
                UserRole.role_name == ADMIN_ROLE,
            )
        )
        if has_admin_role is None:
            await self.redis.delete(session_key(token))
            raise AuthenticationFailed

        return user

    async def logout(self, token: str, user_id: UUID, client_ip: str) -> None:
        """Revoke one bearer session and record the successful logout."""
        await self.redis.delete(session_key(token))
        await self.redis.srem(f"user-service:user-sessions:{user_id}", session_key(token))
        self.session.add(
            SecurityAuditEvent(
                actor_user_id=user_id,
                target_user_id=user_id,
                event_type="auth.logout",
                source_ip=client_ip,
            )
        )
        await self.session.commit()

    async def bootstrap_admin(
        self,
        email: str,
        full_name: str,
        password: str,
    ) -> User:
        """Create the initial admin exactly once after validating account state."""
        validate_password(password)
        await self.session.execute(
            text("SELECT pg_advisory_xact_lock(:lock_id)"), {"lock_id": 74192381}
        )
        existing_admin = await self.session.scalar(
            select(UserRole.user_id).where(UserRole.role_name == ADMIN_ROLE).limit(1)
        )
        if existing_admin is not None:
            raise ValueError("An administrator already exists; bootstrap is disabled.")

        normalized_email = email.casefold()
        user = await self.session.scalar(select(User).where(User.email == normalized_email))
        if user is None:
            user = User(email=normalized_email, full_name=full_name.strip())
            self.session.add(user)
            await self.session.flush()
        elif not user.is_active:
            raise ValueError("Cannot bootstrap an inactive user.")

        credential = await self.session.get(LocalCredential, user.id)
        if credential is not None:
            raise ValueError("A local credential already exists for this user.")

        role = await self.session.get(AuthRole, ADMIN_ROLE)
        if role is None:
            raise RuntimeError("The administrator role is missing; apply database migrations.")

        self.session.add(
            LocalCredential(
                user_id=user.id,
                password_hash=await to_thread(hash_password, password),
            )
        )
        self.session.add(UserRole(user_id=user.id, role_name=ADMIN_ROLE, assigned_by=user.id))
        self.session.add(
            SecurityAuditEvent(
                actor_user_id=user.id,
                target_user_id=user.id,
                event_type="auth.admin.bootstrap",
            )
        )
        await self.session.commit()
        return user

    async def grant_admin(
        self,
        actor_email: str,
        actor_password: str,
        target_user_id: UUID,
        target_password: str,
        source_ip: str | None = None,
    ) -> User:
        """Grant admin to another active user after password reauthentication."""
        await self.session.execute(
            text("SELECT pg_advisory_xact_lock(:lock_id)"), {"lock_id": 74192381}
        )
        validate_password(target_password)
        actor = await self.session.scalar(select(User).where(User.email == actor_email.casefold()))
        actor_credential = (
            await self.session.get(LocalCredential, actor.id) if actor is not None else None
        )
        actor_has_role = (
            await self.session.scalar(
                select(UserRole.user_id).where(
                    UserRole.user_id == actor.id,
                    UserRole.role_name == ADMIN_ROLE,
                )
            )
            if actor is not None
            else None
        )
        valid_actor_password = (
            await to_thread(
                verify_password,
                actor_credential.password_hash,
                actor_password,
            )
            if actor_credential is not None
            else False
        )
        if (
            actor is None
            or not actor.is_active
            or actor_credential is None
            or not actor_credential.is_enabled
            or not valid_actor_password
            or actor_has_role is None
        ):
            raise AuthenticationFailed

        target = await self.session.get(User, target_user_id)
        if target is None or not target.is_active:
            raise ValueError("The target user does not exist or is inactive.")
        if target.id == actor.id:
            raise ValueError(
                "Administrators cannot use role grant to rotate their own credentials."
            )

        target_credential = await self.session.get(LocalCredential, target.id)
        if target_credential is None:
            target_credential = LocalCredential(
                user_id=target.id,
                password_hash=await to_thread(hash_password, target_password),
            )
            self.session.add(target_credential)
        else:
            target_credential.password_hash = await to_thread(hash_password, target_password)
            target_credential.is_enabled = True
            target_credential.session_version += 1

        existing_role = await self.session.get(UserRole, (target.id, ADMIN_ROLE))
        if existing_role is None:
            self.session.add(
                UserRole(
                    user_id=target.id,
                    role_name=ADMIN_ROLE,
                    assigned_by=actor.id,
                )
            )
        self.session.add(
            SecurityAuditEvent(
                actor_user_id=actor.id,
                target_user_id=target.id,
                event_type="auth.admin.granted",
                source_ip=source_ip,
            )
        )
        await self.session.commit()
        return target

    async def revoke_admin(
        self,
        actor_email: str,
        actor_password: str,
        target_user_id: UUID,
        source_ip: str | None = None,
    ) -> None:
        """Revoke another admin role while preserving at least one active admin."""
        await self.session.execute(
            text("SELECT pg_advisory_xact_lock(:lock_id)"), {"lock_id": 74192381}
        )
        actor = await self.session.scalar(select(User).where(User.email == actor_email.casefold()))
        actor_credential = (
            await self.session.get(LocalCredential, actor.id) if actor is not None else None
        )
        valid_actor_password = (
            await to_thread(
                verify_password,
                actor_credential.password_hash,
                actor_password,
            )
            if actor_credential is not None
            else False
        )
        actor_has_role = (
            await self.session.scalar(
                select(UserRole.user_id).where(
                    UserRole.user_id == actor.id,
                    UserRole.role_name == ADMIN_ROLE,
                )
            )
            if actor is not None
            else None
        )
        if (
            actor is None
            or not actor.is_active
            or actor_credential is None
            or not actor_credential.is_enabled
            or not valid_actor_password
            or actor_has_role is None
        ):
            raise AuthenticationFailed
        if actor.id == target_user_id:
            raise ValueError("Administrators cannot revoke their own role.")

        target = await self.session.get(User, target_user_id)
        if target is None:
            raise ValueError("The target user does not exist.")
        target_role = await self.session.get(UserRole, (target.id, ADMIN_ROLE))
        if target_role is None:
            raise ValueError("The target user is not an administrator.")

        if target.is_active:
            active_admin_count = await self.session.scalar(
                select(func.count())
                .select_from(UserRole)
                .join(User, User.id == UserRole.user_id)
                .where(
                    UserRole.role_name == ADMIN_ROLE,
                    User.is_active.is_(True),
                )
            )
            if active_admin_count is not None and active_admin_count <= 1:
                raise ValueError("The last active administrator cannot be revoked.")

        await self.session.delete(target_role)
        target_credential = await self.session.get(LocalCredential, target.id)
        if target_credential is not None:
            target_credential.session_version += 1
        self.session.add(
            SecurityAuditEvent(
                actor_user_id=actor.id,
                target_user_id=target.id,
                event_type="auth.admin.revoked",
                source_ip=source_ip,
            )
        )
        await self.session.commit()
        await self.revoke_user_sessions(target.id)

    async def rotate_password(
        self,
        email: str,
        current_password: str,
        new_password: str,
    ) -> None:
        """Verify the current password, rotate its hash, and revoke prior sessions."""
        validate_password(new_password)
        user = await self.session.scalar(select(User).where(User.email == email.casefold()))
        credential = await self.session.get(LocalCredential, user.id) if user is not None else None
        if (
            user is None
            or not user.is_active
            or credential is None
            or not credential.is_enabled
            or not await to_thread(
                verify_password,
                credential.password_hash,
                current_password,
            )
        ):
            raise AuthenticationFailed

        credential.password_hash = await to_thread(hash_password, new_password)
        credential.session_version += 1
        self.session.add(
            SecurityAuditEvent(
                actor_user_id=user.id,
                target_user_id=user.id,
                event_type="auth.password.rotated",
            )
        )
        await self.session.commit()
        await self.revoke_user_sessions(user.id)

    async def recent_audit_events(self, limit: int) -> list[SecurityAuditEvent]:
        """Return the newest security events, bounded by the caller's limit."""
        result = await self.session.scalars(
            select(SecurityAuditEvent)
            .order_by(SecurityAuditEvent.occurred_at.desc(), SecurityAuditEvent.id)
            .limit(limit)
        )
        return list(result.all())

    async def ensure_admin_account_can_change(
        self,
        target_user_id: UUID,
        actor_user_id: UUID,
        event_type: str,
        source_ip: str | None = None,
    ) -> bool:
        """Lock and validate an admin mutation, recording audit and version changes."""
        await self.session.execute(
            text("SELECT pg_advisory_xact_lock(:lock_id)"),
            {"lock_id": 74192381},
        )
        target = await self.session.get(User, target_user_id)
        if target is None:
            return False
        target_is_admin = await self.session.scalar(
            select(UserRole.user_id).where(
                UserRole.user_id == target_user_id,
                UserRole.role_name == ADMIN_ROLE,
            )
        )
        if target_is_admin is None:
            return False
        if target_user_id == actor_user_id:
            raise AdministratorInvariantError(
                "Administrators cannot disable or delete their own account."
            )

        if target.is_active:
            active_admin_count = await self.session.scalar(
                select(func.count())
                .select_from(UserRole)
                .join(User, User.id == UserRole.user_id)
                .where(
                    UserRole.role_name == ADMIN_ROLE,
                    User.is_active.is_(True),
                )
            )
            if active_admin_count is not None and active_admin_count <= 1:
                raise AdministratorInvariantError(
                    "The last active administrator must remain active."
                )

        credential = await self.session.get(LocalCredential, target_user_id)
        if credential is not None:
            credential.session_version += 1

        self.session.add(
            SecurityAuditEvent(
                actor_user_id=actor_user_id,
                target_user_id=target_user_id,
                event_type=event_type,
                source_ip=source_ip,
            )
        )
        return True

    async def revoke_user_sessions(self, user_id: UUID) -> None:
        """Delete all Redis sessions indexed for a user."""
        await self.redis.eval(
            REVOKE_USER_SESSIONS,
            1,
            f"user-service:user-sessions:{user_id}",
        )
