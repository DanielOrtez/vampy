from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.dependency import AuthServiceDep, CurrentUser
from app.auth.exceptions import InvalidRefreshToken
from app.auth.helpers import clear_refresh_cookie, create_refresh_cookie
from app.auth.schemas import AccessToken
from app.core.config import get_settings
from app.users.schemas import UserRead

settings = get_settings()
auth_router = APIRouter(tags=["auth"], prefix=settings.api_v1_auth_prefix)


@auth_router.post("/login")
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AuthServiceDep,
    response: Response,
) -> AccessToken:
    tokens = await service.login(form.username, form.password)

    response.set_cookie(**create_refresh_cookie(tokens.refresh_token))

    return tokens.access_token


@auth_router.post("/refresh")
async def refresh(
    service: AuthServiceDep,
    response: Response,
    refresh_token: Annotated[str | None, Cookie()] = None,
) -> AccessToken:
    tokens = await service.refresh_token(refresh_token)

    response.set_cookie(**create_refresh_cookie(tokens.refresh_token))

    return tokens.access_token


@auth_router.post("/logout", status_code=204)
async def logout(
    service: AuthServiceDep,
    response: Response,
    refresh_token: Annotated[str | None, Cookie()] = None,
) -> None:
    try:
        await service.logout(refresh_token)
    except InvalidRefreshToken:
        pass

    response.delete_cookie(**clear_refresh_cookie())


@auth_router.get("/me")
def me(current_user: CurrentUser) -> UserRead:
    return current_user
