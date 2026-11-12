"""Authenticated local-only CRUD and validation workload for Locust."""

import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from locust import HttpUser, between, events, task
from locust.exception import LocustError

from tests.performance.analysis import stats_snapshot
from tests.performance.safety import (
    MAX_DURATION_SECONDS,
    MAX_USERS,
    validate_load_profile,
)

REPORT_DIR = Path(os.getenv("PERF_REPORT_DIR", "reports"))
_duplicate_email = f"load-conflict-{uuid4().hex}@example.test"


@events.init.add_listener
def enforce_safe_local_profile(environment, **kwargs) -> None:
    """Reject unsafe load profiles during initialization, before users can spawn."""
    options = environment.parsed_options
    try:
        validate_load_profile(
            environment.host or "",
            int(getattr(options, "num_users", 0)),
            getattr(options, "run_time", None),
        )
    except (TypeError, ValueError) as error:
        raise LocustError(str(error)) from error


@events.test_stop.add_listener
def write_performance_summary(environment, **kwargs) -> None:
    """Write endpoint-level and aggregate Locust metrics to a JSON report."""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    runner_stats = environment.runner.stats
    entries = {
        f"{method} {name}": stats_snapshot(stats)
        for (name, method), stats in sorted(
            runner_stats.entries.items(),
            key=lambda item: (item[0][1] or "", item[0][0]),
        )
    }
    summary = {
        "generated_at": datetime.now(UTC).isoformat(),
        "target": environment.host,
        "safety_limits": {
            "max_virtual_users": MAX_USERS,
            "max_duration_seconds": MAX_DURATION_SECONDS,
            "target_scope": "localhost/loopback only",
        },
        "total": stats_snapshot(runner_stats.total),
        "requests_by_endpoint": entries,
    }
    report_path = REPORT_DIR / "load-summary.json"
    report_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"\nPerformance summary: {report_path}", file=sys.stderr)


def _unexpected_status_message(response, expected: int) -> str:
    """Explain both unexpected HTTP responses and failures before an HTTP response."""
    if response.status_code == 0:
        error = getattr(response, "error", None)
        if error is not None:
            return (
                f"expected HTTP {expected}, but no HTTP response was received: "
                f"{type(error).__name__}: {error}"
            )
        return f"expected HTTP {expected}, but no HTTP response was received (status 0)"
    return f"expected HTTP {expected}, got {response.status_code}"


def _expect_status(response, expected: int) -> None:
    """Mark a Locust response successful only when its status matches."""
    if response.status_code != expected:
        response.failure(_unexpected_status_message(response, expected))
    else:
        response.success()


class UserApiLoad(HttpUser):
    """Exercise authenticated profile CRUD, pagination, and invalid requests."""

    wait_time = between(0.05, 0.25)

    def on_start(self) -> None:
        """Require and install the short-lived admin token for this worker."""
        token = os.environ.get("PERF_AUTH_TOKEN")
        if not token:
            raise LocustError("Set PERF_AUTH_TOKEN to an admin session for the local test service.")

        # Locust's session can bypass environment CA discovery; configure the
        # dedicated test CA explicitly while keeping certificate verification on.
        self.client.verify = os.environ.get("REQUESTS_CA_BUNDLE", True)
        self.client.headers.update({"Authorization": f"Bearer {token}"})

    @task(5)
    def create_read_update_delete_lifecycle(self) -> None:
        """Create, read, update, and delete an isolated profile."""
        email = f"load-{uuid4().hex}@example.test"
        with self.client.post(
            "/users",
            json={"email": email, "full_name": "Load Test User"},
            name="POST /users [create]",
            catch_response=True,
        ) as response:
            if response.status_code != 201:
                response.failure(_unexpected_status_message(response, 201))
                return
            user_id = response.json()["id"]
            response.success()

        with self.client.get(
            f"/users/{user_id}",
            name="GET /users/{user_id} [existing]",
            catch_response=True,
        ) as response:
            _expect_status(response, 200)

        with self.client.patch(
            f"/users/{user_id}",
            json={"full_name": "Updated Load Test User"},
            name="PATCH /users/{user_id}",
            catch_response=True,
        ) as response:
            _expect_status(response, 200)

        with self.client.delete(
            f"/users/{user_id}",
            name="DELETE /users/{user_id}",
            catch_response=True,
        ) as response:
            _expect_status(response, 204)

    @task(4)
    def list_users_at_pagination_boundaries(self) -> None:
        """Exercise valid and invalid pagination boundaries."""
        for query, expected, label in (
            ("?offset=0&limit=1", 200, "first-page"),
            ("?offset=0&limit=100", 200, "max-page"),
            ("?offset=1000000000&limit=100", 200, "empty-page"),
            ("?offset=-1&limit=100", 422, "negative-offset"),
            ("?offset=0&limit=0", 422, "zero-limit"),
            ("?offset=0&limit=101", 422, "over-max-limit"),
        ):
            with self.client.get(
                f"/users{query}",
                name=f"GET /users [pagination:{label}]",
                catch_response=True,
            ) as response:
                _expect_status(response, expected)

    @task(3)
    def request_missing_or_malformed_users(self) -> None:
        """Check malformed identifiers and valid-but-missing user UUIDs."""
        for path, expected, label in (
            ("/users/not-a-uuid", 422, "malformed-id"),
            (f"/users/{uuid4()}", 404, "missing-id"),
        ):
            with self.client.get(
                path,
                name=f"GET /users/{{user_id}} [{label}]",
                catch_response=True,
            ) as response:
                _expect_status(response, expected)

    @task(2)
    def submit_invalid_user_payloads(self) -> None:
        """Exercise rejected create payloads without persisting user data."""
        invalid_payloads = (
            {"email": "not-an-email", "full_name": "Invalid Email"},
            {"email": f"load-{uuid4().hex}@example.test", "full_name": ""},
            {
                "email": f"load-{uuid4().hex}@example.test",
                "full_name": "x" * 121,
            },
            {
                "email": f"load-{uuid4().hex}@example.test",
                "full_name": "Unknown field",
                "unexpected": True,
            },
            {},
        )
        for payload in invalid_payloads:
            with self.client.post(
                "/users",
                json=payload,
                name="POST /users [invalid-payload]",
                catch_response=True,
            ) as response:
                _expect_status(response, 422)

    @task(2)
    def contend_for_duplicate_email(self) -> None:
        """Race users against a shared email and accept one create plus conflicts."""
        with self.client.post(
            "/users",
            json={"email": _duplicate_email, "full_name": "Shared Conflict Case"},
            name="POST /users [concurrent-duplicate-email]",
            catch_response=True,
        ) as response:
            if response.status_code not in {201, 409}:
                expected = "HTTP 201 or 409"
                if response.status_code == 0:
                    error = getattr(response, "error", None)
                    detail = f": {type(error).__name__}: {error}" if error else ""
                    response.failure(
                        f"expected {expected}, but no HTTP response was received{detail}"
                    )
                else:
                    response.failure(f"expected {expected}, got {response.status_code}")
            else:
                response.success()

    @task(1)
    def create_user_at_field_boundaries(self) -> None:
        """Test the minimum/maximum accepted names and clean up created profiles."""
        for full_name, expected, label in (
            (" ", 422, "blank-after-trim"),
            ("x", 201, "minimum-name"),
            ("x" * 120, 201, "maximum-name"),
        ):
            email = f"load-{uuid4().hex}@example.test"
            with self.client.post(
                "/users",
                json={"email": email, "full_name": full_name},
                name=f"POST /users [boundary:{label}]",
                catch_response=True,
            ) as response:
                if response.status_code != expected:
                    response.failure(_unexpected_status_message(response, expected))
                    continue
                if response.status_code == 201:
                    user_id = response.json()["id"]
                    response.success()
                    self.client.delete(
                        f"/users/{user_id}",
                        name="DELETE /users/{user_id} [boundary-cleanup]",
                    )
                else:
                    response.success()
