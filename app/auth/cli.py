"""Interactive, non-echoing local administrator credential management CLI."""

import argparse
import asyncio
from getpass import getpass
from typing import Literal
from uuid import UUID

from pydantic import EmailStr, TypeAdapter, ValidationError

from app.auth.service import AuthService, AuthenticationFailed
from app.core.config import settings
from app.db.session import SessionFactory
from redis.asyncio import Redis


email_adapter = TypeAdapter(EmailStr)


def _read_email(prompt: str) -> str:
    """Read, validate, and normalize an email address from the terminal."""
    value = input(prompt).strip()
    try:
        return str(email_adapter.validate_python(value)).casefold()
    except ValidationError as error:
        raise ValueError("A valid email address is required.") from error


def _read_new_password() -> str:
    """Prompt twice for a password without displaying either value."""
    password = getpass("New administrator password (not echoed): ")
    confirmation = getpass("Confirm password: ")
    if password != confirmation:
        raise ValueError("Passwords do not match.")
    return password


async def _run_command(
    command: Literal["bootstrap-admin", "grant-admin", "rotate-password"], user_id: UUID | None
) -> None:
    """Run a credential-management command and close its Redis client."""
    redis_client = Redis.from_url(
        settings.redis_url,
        decode_responses=True,
        socket_connect_timeout=5,
        socket_timeout=5,
        health_check_interval=30,
    )
    try:
        async with SessionFactory() as session:
            service = AuthService(session, redis_client)
            if command == "bootstrap-admin":
                email = _read_email("Administrator email: ")
                full_name = input("Administrator display name: ").strip()
                if not full_name:
                    raise ValueError("Display name is required.")
                await service.bootstrap_admin(email, full_name, _read_new_password())
                print("Initial administrator created.")
            elif command == "grant-admin":
                if user_id is None:
                    raise ValueError("A target user UUID is required.")
                actor_email = _read_email("Current administrator email: ")
                actor_password = getpass("Current administrator password (not echoed): ")
                await service.grant_admin(
                    actor_email=actor_email,
                    actor_password=actor_password,
                    target_user_id=user_id,
                    target_password=_read_new_password(),
                )
                print("Administrator role assigned.")
            else:
                email = _read_email("Administrator email: ")
                current_password = getpass("Current password (not echoed): ")
                await service.rotate_password(
                    email,
                    current_password,
                    _read_new_password(),
                )
                print("Password rotated; prior sessions have been revoked.")
    finally:
        await redis_client.aclose()


def main() -> None:
    """Parse safe admin CLI commands and report expected validation failures."""
    parser = argparse.ArgumentParser(
        description="Secure local administrator provisioning; no passwords are accepted as arguments."
    )
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser(
        "bootstrap-admin",
        help="Create the first administrator only when no administrator exists.",
    )
    grant_parser = commands.add_parser(
        "grant-admin",
        help="Grant admin after existing administrator password reauthentication.",
    )
    grant_parser.add_argument("user_id", type=UUID)
    commands.add_parser(
        "rotate-password",
        help="Rotate an administrator password after current-password verification.",
    )
    args = parser.parse_args()

    try:
        asyncio.run(_run_command(args.command, getattr(args, "user_id", None)))
    except (ValueError, AuthenticationFailed) as error:
        parser.exit(2, f"{error}\n")


if __name__ == "__main__":
    main()
