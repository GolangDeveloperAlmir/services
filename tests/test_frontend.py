"""HTTP tests for serving the administrator frontend and its static assets."""

from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient

from app.auth.dependencies import get_identity_provider, require_admin
from app.auth.interfaces import Principal
from app.core.config import settings
from app.main import app
from app.media import router as media_router


def test_frontend_and_assets_are_served_over_https() -> None:
    """Serve the HTML entry point and compiled assets from the API origin."""
    client = TestClient(app, base_url="https://localhost")

    page = client.get("/")
    stylesheet = client.get("/assets/styles.css")
    script = client.get("/assets/app.js")

    assert page.status_code == 200
    assert "text/html" in page.headers["content-type"]
    assert 'id="login-form"' in page.text
    assert stylesheet.status_code == 200
    assert "text/css" in stylesheet.headers["content-type"]
    assert script.status_code == 200
    assert "text/javascript" in script.headers["content-type"]
    assert "Content-Security-Policy" in page.headers


def test_frontend_is_not_served_over_cleartext_http() -> None:
    """Require HTTPS for the HTML entry point just like protected API routes."""
    client = TestClient(app, base_url="http://localhost")

    response = client.get("/")

    assert response.status_code == 426


def test_untrusted_client_cannot_spoof_forwarded_https() -> None:
    """Ignore forwarded-proto headers from clients outside the proxy allowlist."""
    client = TestClient(
        app,
        base_url="http://localhost",
        client=("203.0.113.8", 12345),
    )

    response = client.get(
        "/",
        headers={"X-Forwarded-Proto": "https", "X-Forwarded-For": "203.0.113.8"},
    )

    assert response.status_code == 426


def test_trusted_proxy_must_send_one_https_client_address(monkeypatch) -> None:
    """Require the configured proxy and reject ambiguous forwarded client IPs."""
    monkeypatch.setattr(settings, "trusted_proxy_ips", ["172.30.240.2"])
    client = TestClient(
        app,
        base_url="http://localhost",
        client=("172.30.240.2", 12345),
    )

    valid = client.get(
        "/",
        headers={"X-Forwarded-Proto": "https", "X-Forwarded-For": "198.51.100.10"},
    )
    ambiguous = client.get(
        "/",
        headers={
            "X-Forwarded-Proto": "https",
            "X-Forwarded-For": "198.51.100.10, 203.0.113.8",
        },
    )

    assert valid.status_code == 200
    assert ambiguous.status_code == 400


def test_media_catalog_is_admin_only_and_serves_only_curated_files(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Serve supported regular files by opaque ID and reject path traversal."""
    monkeypatch.setattr(settings, "media_root", tmp_path)
    monkeypatch.setitem(
        app.dependency_overrides,
        require_admin,
        lambda: Principal("admin", frozenset({"users:admin"}), uuid4()),
    )
    city = tmp_path / "backgrounds" / "city"
    city.mkdir(parents=True)
    (city / "night.png").write_bytes(b"safe test image")
    (city / "ignore.svg").write_text("<svg></svg>", encoding="utf-8")
    client = TestClient(app, base_url="https://localhost")

    catalog = client.get("/media/catalog")
    assert catalog.status_code == 200
    items = catalog.json()
    assert len(items) == 1
    assert items[0]["category"] == "city"
    assert items[0]["kind"] == "background"

    asset = client.get(items[0]["url"])
    traversal = client.get("/media/../../etc/passwd")

    assert asset.status_code == 200
    assert asset.headers["content-type"] == "image/png"
    assert asset.content == b"safe test image"
    assert asset.headers["x-content-type-options"] == "nosniff"
    assert asset.headers["cache-control"] == "private, no-store"
    assert traversal.status_code in {404, 422}


def test_media_catalog_requires_admin(monkeypatch) -> None:
    """Reject anonymous catalog and media requests."""
    monkeypatch.setitem(app.dependency_overrides, get_identity_provider, lambda: object())
    client = TestClient(app, base_url="https://localhost")

    assert client.get("/media/catalog").status_code == 401
    assert client.get(f"/media/{'0' * 32}").status_code == 401


def test_media_catalog_rejects_oversized_items_and_catalogs(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Keep media responses bounded and fail explicitly when the catalog is too large."""
    monkeypatch.setattr(settings, "media_root", tmp_path)
    monkeypatch.setattr(media_router, "MAX_MEDIA_BYTES", 1)
    monkeypatch.setattr(media_router, "MAX_CATALOG_ITEMS", 1)
    monkeypatch.setitem(
        app.dependency_overrides,
        require_admin,
        lambda: Principal("admin", frozenset({"users:admin"}), uuid4()),
    )
    city = tmp_path / "backgrounds" / "city"
    city.mkdir(parents=True)
    (city / "oversized.png").write_bytes(b"xx")
    client = TestClient(app, base_url="https://localhost")

    assert client.get("/media/catalog").json() == []

    (city / "second.png").write_bytes(b"x")
    (city / "third.png").write_bytes(b"x")

    assert client.get("/media/catalog").status_code == 503
