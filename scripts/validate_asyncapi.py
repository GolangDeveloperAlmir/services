"""Validate the repository AsyncAPI document against its bundled JSON schema."""

import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft7Validator, FormatChecker
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT7


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "asyncapi-3.0.0.json"
DOCUMENT_PATH = ROOT / "asyncapi.yaml"


def _walk(value: Any):
    """Yield every nested mapping in a JSON-schema document."""
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def validate_asyncapi() -> list[str]:
    """Return sorted validation errors, or an empty list for a valid document."""
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    document = yaml.safe_load(DOCUMENT_PATH.read_text(encoding="utf-8"))
    Draft7Validator.check_schema(schema)

    resources = {
        node["$id"]: Resource.from_contents(node, default_specification=DRAFT7)
        for node in _walk(schema)
        if isinstance(node, dict) and isinstance(node.get("$id"), str)
    }
    registry = Registry().with_resources(resources.items())
    validator = Draft7Validator(
        schema,
        registry=registry,
        format_checker=FormatChecker(),
    )
    errors = sorted(
        validator.iter_errors(document),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )

    return [
        f"{'.'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in errors
    ]


def main() -> int:
    """Print AsyncAPI validation results and return a process exit code."""
    errors = validate_asyncapi()
    if errors:
        print("AsyncAPI validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("AsyncAPI document is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
