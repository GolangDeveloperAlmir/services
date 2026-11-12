"""Tests for loopback-only Locust targets and bounded load profiles."""

import pytest

from tests.performance.safety import MAX_DURATION_SECONDS, validate_load_profile


@pytest.mark.parametrize(
    "host",
    [
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://[::1]:8000",
    ],
)
@pytest.mark.parametrize("duration", ["30s", 30, 30.0])
def test_load_profile_accepts_loopback_targets(host: str, duration: str | float) -> None:
    """Allow localhost and IPv4/IPv6 loopback endpoints with Locust's parsed seconds."""
    validate_load_profile(host, users=10, duration=duration)


@pytest.mark.parametrize(
    "host",
    [
        "https://example.com",
        "http://192.168.1.10:8000",
        "http://127.0.0.1:8000/path",
        "http://user:password@127.0.0.1:8000",
    ],
)
def test_load_profile_rejects_non_local_or_ambiguous_targets(host: str) -> None:
    """Reject remote targets, paths, and user-info in load-test URLs."""
    with pytest.raises(ValueError):
        validate_load_profile(host, users=10, duration="30s")


@pytest.mark.parametrize(
    ("users", "duration"),
    [
        (0, "30s"),
        (251, "30s"),
        (10, "16m"),
        (10, "indefinite"),
        (10, 0),
        (10, MAX_DURATION_SECONDS + 1),
        (10, float("inf")),
        (10, float("nan")),
        (10, True),
    ],
)
def test_load_profile_enforces_user_and_duration_caps(
    users: int,
    duration: str | float,
) -> None:
    """Enforce finite runs and the configured maximum virtual-user count."""
    with pytest.raises(TypeError if isinstance(duration, bool) else ValueError):
        validate_load_profile("http://127.0.0.1:8000", users, duration)
