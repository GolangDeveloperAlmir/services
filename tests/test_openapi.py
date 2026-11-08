"""Smoke tests for important paths in the runtime OpenAPI schema."""

from fastapi.routing import APIRoute

from app.auth.router import router as auth_router
from app.core.config import settings
from app.media.router import router as media_router
from app.main import app
from app.users.router import router as users_router


def test_openapi_contains_user_routes() -> None:
    """Expose the configured service title and both user route shapes."""
    schema = app.openapi()

    assert schema["info"]["title"] == settings.app_name
    assert "/users" in schema["paths"]
    assert "/users/{user_id}" in schema["paths"]


def test_every_public_api_route_is_in_openapi() -> None:
    """Keep every registered public API method and path in the OpenAPI contract."""
    routes = {
        (route.path, method.lower())
        for router in (auth_router, media_router, users_router)
        for route in router.routes
        if isinstance(route, APIRoute) and route.include_in_schema
        for method in route.methods or ()
    }
    documented = {
        (path, method) for path, path_item in app.openapi()["paths"].items() for method in path_item
    }

    assert routes == documented
