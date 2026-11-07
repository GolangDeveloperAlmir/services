"""Regenerate the checked-in OpenAPI snapshot from the FastAPI application."""

from pathlib import Path

import yaml

from app.main import app


ROOT = Path(__file__).resolve().parents[1]
OPENAPI_PATH = ROOT / "openapi.yaml"


def main() -> None:
    """Write the current runtime OpenAPI schema to ``openapi.yaml``."""
    schema = app.openapi()
    OPENAPI_PATH.write_text(
        yaml.safe_dump(schema, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    print(f"Wrote {OPENAPI_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
