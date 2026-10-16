from httpx2 import AsyncClient

from app.core.config import get_settings
from app.users.models import User

settings = get_settings()
endpoint = f"{settings.api_v1_prefix}{settings.api_v1_auth_prefix}"


async def test_success_login(client: AsyncClient, user: User) -> None:
    login_data = {"username": user.email, "password": user.plain_password}  # ty: ignore

    r = await client.post(f"{endpoint}/login", data=login_data)
    tokens = r.json()

    assert r.status_code == 200
    assert type(tokens["access_token"]) is str
    assert type(tokens["expires_in"]) is int
    assert tokens["token_type"] == "Bearer"


async def test_wrong_password(client: AsyncClient, user: User) -> None:
    wrong_password = f"{user.plain_password}@@@@"  # ty:ignore
    login_data = {"username": user.email, "password": wrong_password}

    r = await client.post(f"{endpoint}/login", data=login_data)

    result = r.json()
    assert r.status_code == 401
    assert result["error"] == "invalid_credentials"
    assert "detail" in result


async def test_wrong_email(client: AsyncClient, user: User) -> None:
    login_data = {"username": "test", "password": user.plain_password}  # ty: ignore

    r = await client.post(f"{endpoint}/login", data=login_data)

    result = r.json()
    assert r.status_code == 401
    assert result["error"] == "invalid_credentials"
    assert "detail" in result
