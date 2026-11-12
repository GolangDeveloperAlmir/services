"""Service and HTTP regression tests for all profile CRUD operations."""

import asyncio
from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_auth_service, require_admin
from app.auth.interfaces import Principal
from app.main import app
from app.users.exceptions import EmailAlreadyExistsError, UserNotFoundError
from app.users.model import User
from app.users.repository import UserRepository
from app.users.router import get_user_service
from app.users.schemas import UserCreate, UserUpdate
from app.users.service import UserService


class MemoryUserRepository(UserRepository):
    """In-memory repository substitute for isolated service tests."""

    def __init__(
        self,
        session: AsyncSession,
        users: list[User] | None = None,
    ) -> None:
        """Initialize the test repository with a session and optional rows."""
        super().__init__(session)
        self.users = users or []
        self.deleted: list[User] = []

    async def get_by_id(self, user_id: UUID) -> User | None:
        """Find a profile by identifier in the in-memory collection."""
        return next((user for user in self.users if user.id == user_id), None)

    async def get_by_email(self, email: str) -> User | None:
        """Find a profile by its normalized email address."""
        return next((user for user in self.users if user.email == email), None)

    async def get_all(self, offset: int, limit: int) -> list[User]:
        """Return the requested slice of in-memory profiles."""
        return self.users[offset : offset + limit]

    def add(self, user: User) -> None:
        """Add a profile to the in-memory collection."""
        self.users.append(user)

    async def delete(self, user: User) -> None:
        """Remove and record a profile deleted by the service."""
        self.users.remove(user)
        self.deleted.append(user)


def build_service(
    users: list[User] | None = None,
) -> tuple[UserService, AsyncMock, MemoryUserRepository]:
    """Build a user service with a mocked session and in-memory repository."""
    session = AsyncMock()
    session.add = Mock()
    service = UserService(session)
    repository = MemoryUserRepository(session, users)
    service.repository = repository
    return service, session, repository


def make_user(
    *,
    user_id: UUID | None = None,
    email: str = "person@example.com",
    full_name: str = "Example Person",
) -> User:
    """Construct a profile model with deterministic defaults for CRUD tests."""
    now = datetime.now(UTC)
    return User(
        id=user_id or uuid4(),
        email=email,
        full_name=full_name,
        is_active=True,
        created_at=now,
        updated_at=now,
    )


def test_repository_lists_users_in_stable_newest_first_order() -> None:
    """Ensure repository pagination uses stable newest-first SQL ordering."""
    users = [make_user()]
    session = AsyncMock()
    session.scalars.return_value = SimpleNamespace(all=Mock(return_value=users))
    repository = UserRepository(session)

    result = asyncio.run(repository.get_all(offset=20, limit=10))

    statement = session.scalars.await_args.args[0]
    sql = str(statement)
    assert result == users
    assert "ORDER BY users.created_at DESC, users.id" in sql
    assert "LIMIT" in sql
    assert "OFFSET" in sql


def test_user_service_create_normalizes_email_and_commits() -> None:
    """Create and commit a profile using trimmed fields and canonical email."""
    service, session, repository = build_service()
    actor_id = uuid4()

    created = asyncio.run(
        service.create(
            UserCreate(email=" Person@Example.com ", full_name=" Example Person "),
            actor_user_id=actor_id,
            source_ip="10.0.0.10",
        )
    )

    assert created.email == "person@example.com"
    assert created.full_name == "Example Person"
    assert repository.users == [created]
    session.flush.assert_awaited_once()
    session.commit.assert_awaited_once()
    session.refresh.assert_awaited_once_with(created)
    event = session.add.call_args.args[0]
    assert event.actor_user_id == actor_id
    assert event.target_user_id == created.id
    assert event.event_type == "user.profile.created"
    assert event.source_ip == "10.0.0.10"


def test_user_service_reads_and_paginates() -> None:
    """Read an existing profile and verify service pagination defaults."""
    first, second = make_user(), make_user()
    service, _, _ = build_service([first, second])

    assert asyncio.run(service.get_by_id(first.id)) is first
    assert asyncio.run(service.get_all(offset=1, limit=1)) == [second]
    assert asyncio.run(service.get_all()) == [first, second]


def test_user_service_missing_user_raises_domain_error() -> None:
    """Raise the domain not-found error for a missing profile identifier."""
    service, _, _ = build_service()

    with pytest.raises(UserNotFoundError, match="User not found"):
        asyncio.run(service.get_by_id(uuid4()))


def test_user_service_updates_profile_and_normalizes_email() -> None:
    """Update profile fields and normalize the supplied email consistently."""
    user = make_user(email="person@example.com")
    service, session, _ = build_service([user])
    actor_id = uuid4()

    updated = asyncio.run(
        service.update(
            user.id,
            UserUpdate(email="PERSON@EXAMPLE.COM", full_name=" Updated Name ", is_active=False),
            actor_user_id=actor_id,
            source_ip="10.0.0.11",
        )
    )

    assert updated is user
    assert user.email == "person@example.com"
    assert user.full_name == "Updated Name"
    assert user.is_active is False
    session.commit.assert_awaited_once()
    session.refresh.assert_awaited_once_with(user)
    event = session.add.call_args.args[0]
    assert event.actor_user_id == actor_id
    assert event.target_user_id == user.id
    assert event.event_type == "user.profile.updated"
    assert event.source_ip == "10.0.0.11"


def test_user_service_rejects_duplicate_email_on_create_and_update() -> None:
    """Reject duplicate email addresses before either mutation is committed."""
    existing, target = make_user(), make_user(email="target@example.com")
    service, session, _ = build_service([existing, target])

    with pytest.raises(EmailAlreadyExistsError, match="Email already exists"):
        asyncio.run(
            service.create(
                UserCreate(email=existing.email, full_name="Another Person"),
                actor_user_id=uuid4(),
            )
        )
    with pytest.raises(EmailAlreadyExistsError, match="Email already exists"):
        asyncio.run(
            service.update(
                target.id,
                UserUpdate(email=existing.email),
                actor_user_id=uuid4(),
            )
        )

    session.add.assert_not_called()
    session.commit.assert_not_awaited()


def test_user_service_delete_removes_existing_user_and_commits() -> None:
    """Delete an existing profile from the repository and commit once."""
    user = make_user()
    service, session, repository = build_service([user])
    actor_id = uuid4()

    asyncio.run(
        service.delete(
            user.id,
            actor_user_id=actor_id,
            source_ip="10.0.0.12",
        )
    )

    assert repository.users == []
    assert repository.deleted == [user]
    session.flush.assert_awaited_once()
    session.commit.assert_awaited_once()
    event = session.add.call_args.args[0]
    assert event.actor_user_id == actor_id
    assert event.target_user_id == user.id
    assert event.event_type == "user.profile.deleted"
    assert event.source_ip == "10.0.0.12"


class MemoryCRUDService:
    """In-memory HTTP dependency that models user CRUD and email conflicts."""

    def __init__(self) -> None:
        """Create an empty profile store for isolated HTTP route tests."""
        self.users: dict[UUID, User] = {}
        self.audit_events: list[tuple[str, UUID, str | None]] = []

    async def create(
        self,
        data: UserCreate,
        *,
        actor_user_id: UUID,
        source_ip: str | None = None,
    ) -> User:
        """Create a profile and reject an email already in the test store."""
        email = str(data.email).casefold()
        if any(user.email.casefold() == email for user in self.users.values()):
            raise EmailAlreadyExistsError
        user = make_user(email=email, full_name=data.full_name)
        self.users[user.id] = user
        self.audit_events.append(("user.profile.created", actor_user_id, source_ip))
        return user

    async def get_all(self, offset: int, limit: int) -> list[User]:
        """Return a paginated, newest-first profile list."""
        users = sorted(self.users.values(), key=lambda user: user.id)
        users.sort(key=lambda user: user.created_at, reverse=True)
        return users[offset : offset + limit]

    async def get_by_id(self, user_id: UUID) -> User:
        """Return a stored profile or raise the domain not-found error."""
        user = self.users.get(user_id)
        if user is None:
            raise UserNotFoundError
        return user

    async def update(
        self,
        user_id: UUID,
        data: UserUpdate,
        *,
        actor_user_id: UUID,
        source_ip: str | None = None,
    ) -> User:
        """Apply validated fields and reject duplicate normalized email."""
        user = await self.get_by_id(user_id)
        changes = data.model_dump(exclude_unset=True)
        if "email" in changes:
            email = str(changes["email"]).casefold()
            if any(
                other.id != user_id and other.email.casefold() == email
                for other in self.users.values()
            ):
                raise EmailAlreadyExistsError
            changes["email"] = email
        for field, value in changes.items():
            setattr(user, field, value)
        self.audit_events.append(("user.profile.updated", actor_user_id, source_ip))
        return user

    async def delete(
        self,
        user_id: UUID,
        *,
        actor_user_id: UUID,
        source_ip: str | None = None,
    ) -> None:
        """Delete a stored profile after verifying that it exists."""
        await self.get_by_id(user_id)
        self.audit_events.append(("user.profile.deleted", actor_user_id, source_ip))
        del self.users[user_id]


@pytest.fixture
def crud_client():
    """Override auth and CRUD dependencies with isolated in-memory fakes."""
    service = MemoryCRUDService()
    auth_service = AsyncMock()
    auth_service.ensure_admin_account_can_change.return_value = False
    previous_overrides = app.dependency_overrides.copy()
    admin_id = uuid4()
    app.dependency_overrides[require_admin] = lambda: Principal(
        "admin",
        frozenset({"users:admin"}),
        admin_id,
    )
    app.dependency_overrides[get_user_service] = lambda: service
    app.dependency_overrides[get_auth_service] = lambda: auth_service
    client = TestClient(app, base_url="https://localhost")
    try:
        yield client, service, auth_service
    finally:
        client.close()
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous_overrides)


def test_user_crud_http_endpoints(crud_client) -> None:
    """Exercise create, list, detail, update, and delete over HTTPS routes."""
    client, service, auth_service = crud_client
    created = client.post(
        "/users",
        json={"email": "person@example.com", "full_name": "Example Person"},
    )
    assert created.status_code == 201
    created_data = created.json()
    user_id = UUID(created_data["id"])
    assert created_data["email"] == "person@example.com"

    listed = client.get("/users?offset=0&limit=1")
    assert listed.status_code == 200
    assert [user["id"] for user in listed.json()] == [str(user_id)]
    assert client.get(f"/users/{user_id}").json()["full_name"] == "Example Person"

    updated = client.patch(
        f"/users/{user_id}",
        json={"full_name": "Updated Person"},
    )
    assert updated.status_code == 200
    assert updated.json()["full_name"] == "Updated Person"

    deleted = client.delete(f"/users/{user_id}")
    assert deleted.status_code == 204
    assert deleted.content == b""
    assert service.users == {}
    assert [event[0] for event in service.audit_events] == [
        "user.profile.created",
        "user.profile.updated",
        "user.profile.deleted",
    ]
    assert {event[1] for event in service.audit_events} == {service.audit_events[0][1]}
    assert all(event[2] is not None for event in service.audit_events)
    auth_service.ensure_admin_account_can_change.assert_awaited_once()


def test_user_crud_http_errors_and_validation(crud_client) -> None:
    """Check not-found responses and invalid CRUD payload and query handling."""
    client, _, _ = crud_client

    missing = client.get(f"/users/{uuid4()}")
    assert missing.status_code == 404
    assert missing.json() == {"detail": "User not found"}

    invalid_create = client.post(
        "/users",
        json={"email": "not-an-email", "full_name": "Person", "is_admin": True},
    )
    assert invalid_create.status_code == 422

    invalid_patch = client.patch(f"/users/{uuid4()}", json={})
    assert invalid_patch.status_code == 422

    invalid_page = client.get("/users?offset=-1")
    assert invalid_page.status_code == 422


def test_user_crud_http_rejects_duplicate_emails(crud_client) -> None:
    """Return conflicts for duplicate emails on create and update requests."""
    client, _, _ = crud_client
    first = client.post(
        "/users",
        json={"email": "duplicate@example.com", "full_name": "First Person"},
    )
    second = client.post(
        "/users",
        json={"email": "second@example.com", "full_name": "Second Person"},
    )
    assert first.status_code == 201
    assert second.status_code == 201

    duplicate_create = client.post(
        "/users",
        json={"email": "DUPLICATE@example.com", "full_name": "Another Person"},
    )
    assert duplicate_create.status_code == 409
    assert duplicate_create.json() == {"detail": "Email already exists"}

    duplicate_update = client.patch(
        f"/users/{second.json()['id']}",
        json={"email": "DUPLICATE@example.com"},
    )
    assert duplicate_update.status_code == 409
    assert duplicate_update.json() == {"detail": "Email already exists"}
