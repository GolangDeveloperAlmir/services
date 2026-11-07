from app.core.config import settings
from app.main import app


def test_openapi_contains_user_routes() -> None:
    schema = app.openapi()

    assert schema["info"]["title"] == settings.app_name
    assert "/users" in schema["paths"]
    assert "/users/{user_id}" in schema["paths"]
