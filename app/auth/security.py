"""Password rules and token/key derivation primitives for local authentication."""

import re
import secrets
from hashlib import sha256

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError


PASSWORD_HASHER = PasswordHasher()
MIN_PASSWORD_LENGTH = 15
MAX_PASSWORD_LENGTH = 128


def validate_password(password: str) -> None:
    """Enforce password length, encoding, whitespace, and common-password rules."""
    if not MIN_PASSWORD_LENGTH <= len(password) <= MAX_PASSWORD_LENGTH:
        raise ValueError(
            f"Password must be between {MIN_PASSWORD_LENGTH} and {MAX_PASSWORD_LENGTH} characters."
        )
    if len(password.encode("utf-8")) > 1024:
        raise ValueError("Password exceeds the maximum supported byte length.")
    if password.strip() != password:
        raise ValueError("Password must not begin or end with whitespace.")
    normalized = re.sub(r"[^a-z0-9]", "", password.lower())
    common_passwords = {
        "passwordpassword",
        "qwertyuiopasdf",
        "letmeinletmein",
        "adminadminadmin",
        "changemechangeme",
    }
    if normalized in common_passwords:
        raise ValueError("Choose a less common password.")


def hash_password(password: str) -> str:
    """Validate and hash a password using the configured Argon2id hasher."""
    validate_password(password)
    return PASSWORD_HASHER.hash(password)


def verify_password(password_hash: str, password: str) -> bool:
    """Verify a password hash, returning false for mismatch or invalid hashes."""
    try:
        return PASSWORD_HASHER.verify(password_hash, password)
    except VerifyMismatchError, VerificationError, InvalidHashError:
        return False


def password_needs_rehash(password_hash: str) -> bool:
    """Report whether a stored password hash uses outdated hasher parameters."""
    return PASSWORD_HASHER.check_needs_rehash(password_hash)


def new_session_token() -> str:
    """Generate an opaque cryptographically secure bearer token."""
    return secrets.token_urlsafe(32)


def session_key(token: str) -> str:
    """Derive a non-reversible Redis key from a bearer token."""
    digest = sha256(token.encode("utf-8")).hexdigest()
    return f"user-service:session:{digest}"


def rate_limit_key(email: str, client_ip: str) -> str:
    """Build a Redis key for the combined normalized email and IP rate limit."""
    digest = sha256(f"{email.casefold()}\0{client_ip}".encode()).hexdigest()
    return f"user-service:login-attempts:{digest}"


def ip_rate_limit_key(client_ip: str) -> str:
    """Build a Redis key for the independent source-IP login limit."""
    digest = sha256(client_ip.encode()).hexdigest()
    return f"user-service:login-ip:{digest}"
