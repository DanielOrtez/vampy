from typing import Any

from app.core.config import get_settings

settings = get_settings()
cookie_path = f"{settings.api_v1_prefix}{settings.api_v1_auth_prefix}"


def create_refresh_cookie(value: str) -> dict[str, Any]:
    return {
        "key": "refresh_token",
        "value": value,
        "httponly": True,
        "secure": settings.is_production,
        "samesite": "strict",
        "max_age": settings.refresh_token_days * 24 * 60 * 60,
        "path": cookie_path,
    }


def clear_refresh_cookie() -> dict[str, Any]:
    return {
        "key": "refresh_token",
        "httponly": True,
        "samesite": "strict",
        "secure": settings.is_production,
        "path": cookie_path,
    }
