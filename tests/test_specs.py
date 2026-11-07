from pathlib import Path

import yaml
from openapi_spec_validator import validate

from app.main import app
from scripts.validate_asyncapi import validate_asyncapi


ROOT = Path(__file__).resolve().parents[1]


def test_openapi_file_is_generated_from_fastapi_and_valid() -> None:
    spec = yaml.safe_load((ROOT / "openapi.yaml").read_text(encoding="utf-8"))

    validate(spec)
    assert spec == app.openapi()


def test_asyncapi_file_documents_current_absence_of_message_channels() -> None:
    spec = yaml.safe_load((ROOT / "asyncapi.yaml").read_text(encoding="utf-8"))

    assert spec["asyncapi"].startswith("3.")
    assert spec["info"]["title"] == "User Service Events"
    assert spec["channels"] == {}
    assert spec["operations"] == {}
    assert validate_asyncapi() == []
