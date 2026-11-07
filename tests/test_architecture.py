import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_ROOT = ROOT / "app"
LAYER_ORDER = {
    "app.main": 0,
    "app.users": 1,
    "app.auth": 2,
    "app.db": 3,
    "app.core": 4,
}


def _module_name(path: Path) -> str:
    relative = path.relative_to(ROOT).with_suffix("")
    parts = relative.parts
    return ".".join(parts[:-1] if parts[-1] == "__init__" else parts)


def _imported_module(node: ast.Import | ast.ImportFrom, module: str) -> list[str]:
    if isinstance(node, ast.Import):
        return [alias.name for alias in node.names]

    if node.level == 0:
        return [node.module] if node.module else []

    current_package = module.split(".")[:-1]
    anchor = current_package[: len(current_package) - node.level + 1]
    imported = ".".join([*anchor, *(node.module.split(".") if node.module else [])])
    return [imported] if imported else []


def _layer_for(module: str) -> str | None:
    for layer in LAYER_ORDER:
        if module == layer or module.startswith(f"{layer}."):
            return layer
    return None


def test_application_imports_follow_inward_layer_order() -> None:
    violations: list[str] = []

    for source_file in APP_ROOT.rglob("*.py"):
        source_module = _module_name(source_file)
        source_layer = _layer_for(source_module)
        if source_layer is None:
            continue

        tree = ast.parse(source_file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, (ast.Import, ast.ImportFrom)):
                continue
            for imported in _imported_module(node, source_module):
                target_layer = _layer_for(imported)
                if (
                    target_layer is not None
                    and LAYER_ORDER[source_layer] > LAYER_ORDER[target_layer]
                ):
                    violations.append(
                        f"{source_module} ({source_layer}) imports {imported} ({target_layer})"
                    )

    assert not violations, "\n".join(violations)


def test_import_linter_configuration_declares_application_layers() -> None:
    config = (ROOT / ".importlinter").read_text(encoding="utf-8")

    assert "type = layers" in config
    assert all(layer in config for layer in LAYER_ORDER)
