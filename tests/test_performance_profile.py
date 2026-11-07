import pytest

from tests.performance.safety import validate_load_profile


@pytest.mark.parametrize(
    "host",
    [
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://[::1]:8000",
    ],
)
def test_load_profile_accepts_loopback_targets(host: str) -> None:
    validate_load_profile(host, users=10, duration="30s")


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
    with pytest.raises(ValueError):
        validate_load_profile(host, users=10, duration="30s")


@pytest.mark.parametrize(
    ("users", "duration"),
    [
        (0, "30s"),
        (251, "30s"),
        (10, "16m"),
        (10, "indefinite"),
    ],
)
def test_load_profile_enforces_user_and_duration_caps(users: int, duration: str) -> None:
    with pytest.raises(ValueError):
        validate_load_profile("http://127.0.0.1:8000", users, duration)
