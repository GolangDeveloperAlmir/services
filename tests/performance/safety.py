"""Local-target and resource-bound validation for performance test profiles."""

import ipaddress
import re
from urllib.parse import urlsplit


MAX_USERS = 250
MAX_DURATION_SECONDS = 15 * 60
_DURATION_PATTERN = re.compile(r"^([1-9]\d*)(s|m|h)$")


def validate_load_profile(host: str, users: int, duration: str) -> None:
    """Reject non-loopback hosts and load profiles beyond hard safety caps."""
    parsed = urlsplit(host)
    if (
        parsed.scheme not in {"http", "https"}
        or parsed.hostname is None
        or parsed.username is not None
        or parsed.password is not None
        or parsed.path not in {"", "/"}
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("Load tests require a plain http(s) URL with no credentials or path.")

    hostname = parsed.hostname.lower()
    if hostname != "localhost":
        try:
            is_loopback = ipaddress.ip_address(hostname).is_loopback
        except ValueError as error:
            raise ValueError("Load tests are restricted to localhost/loopback targets.") from error
        if not is_loopback:
            raise ValueError("Load tests are restricted to localhost/loopback targets.")

    if not 1 <= users <= MAX_USERS:
        raise ValueError(f"Virtual users must be between 1 and {MAX_USERS}.")

    match = _DURATION_PATTERN.fullmatch(duration)
    if match is None:
        raise ValueError("Specify a finite duration such as 30s or 5m.")
    value = int(match.group(1))
    unit = match.group(2)
    duration_seconds = value * {"s": 1, "m": 60, "h": 3600}[unit]
    if duration_seconds > MAX_DURATION_SECONDS:
        raise ValueError(
            f"Test duration must be between 1 second and {MAX_DURATION_SECONDS} seconds."
        )
