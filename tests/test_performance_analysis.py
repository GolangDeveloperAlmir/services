from tests.performance.analysis import stats_snapshot


class FakeRequestStats:
    num_requests = 42
    num_failures = 2
    avg_response_time = 18.345
    median_response_time = 12.0
    max_response_time = 87.6
    current_rps = 3.14159

    def get_response_time_percentile(self, percentile: float) -> float:
        return {0.95: 72.345, 0.99: 84.567}[percentile]


def test_stats_snapshot_reports_request_and_latency_metrics() -> None:
    report = stats_snapshot(FakeRequestStats())

    assert report == {
        "requests": 42,
        "failures": 2,
        "average_ms": 18.34,
        "median_ms": 12.0,
        "p95_ms": 72.34,
        "p99_ms": 84.57,
        "max_ms": 87.6,
        "requests_per_second": 3.14,
    }
