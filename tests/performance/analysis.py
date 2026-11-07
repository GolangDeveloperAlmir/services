"""Extract stable response-time and throughput metrics from Locust statistics."""

from typing import Protocol


class RequestStats(Protocol):
    """Subset of Locust stats required by the report serializer."""

    num_requests: int
    num_failures: int
    avg_response_time: float
    median_response_time: float
    max_response_time: float
    current_rps: float

    def get_response_time_percentile(self, percentile: float) -> float | None:
        """Return one response-time percentile in milliseconds, if available."""
        ...


def stats_snapshot(stats: RequestStats) -> dict[str, int | float]:
    """Serialize aggregate request counters and latency percentiles."""
    return {
        "requests": stats.num_requests,
        "failures": stats.num_failures,
        "average_ms": round(stats.avg_response_time, 2),
        "median_ms": round(stats.median_response_time, 2),
        "p95_ms": round(stats.get_response_time_percentile(0.95) or 0, 2),
        "p99_ms": round(stats.get_response_time_percentile(0.99) or 0, 2),
        "max_ms": round(stats.max_response_time or 0, 2),
        "requests_per_second": round(stats.current_rps, 2),
    }
