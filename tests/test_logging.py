"""Regression tests for structured application request logging."""

import json
import logging

from app.core.logging import JsonFormatter


def test_json_formatter_includes_structured_request_fields() -> None:
    """Keep approved request metadata in the JSON log representation."""
    record = logging.LogRecord(
        name="app.main",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="HTTP request completed",
        args=(),
        exc_info=None,
    )
    record.http_method = "GET"
    record.http_path = "/users"
    record.http_status_code = 200
    record.duration_ms = 1.25

    payload = json.loads(JsonFormatter().format(record))

    assert payload["level"] == "INFO"
    assert payload["message"] == "HTTP request completed"
    assert payload["http_method"] == "GET"
    assert payload["http_path"] == "/users"
    assert payload["http_status_code"] == 200
    assert payload["duration_ms"] == 1.25
