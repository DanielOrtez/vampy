from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.dependency import AuthServiceDep, CurrentUser
from app.auth.exceptions import InvalidCredentials, InvalidRefreshToken
from app.auth.schemas import AccessToken, Tokens
from app.core.config import get_settings
from app.users.schemas import UserRead

settings = get_settings()
auth_router = APIRouter(tags=["auth"], prefix=settings.api_v1_auth_prefix)


def build_token_response(tokens: Tokens, response: Response) -> AccessToken:
    response.set_cookie(
        "refresh_token",
        tokens.refresh_token,
        httponly=True,
        secure=settings.is_production,
        samesite="strict",
        max_age=settings.refresh_token_days * 24 * 60 * 60,
        path=f"{settings.api_v1_prefix}{settings.api_v1_auth_prefix}",
    )
    return tokens.access_token


@auth_router.post("/login")
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AuthServiceDep,
    response: Response,
) -> AccessToken:
    try:
        tokens = await service.login(form.username, form.password)
    except InvalidCredentials as err:
        raise HTTPException(status_code=err.status_code, detail=err.message) from err
    return build_token_response(tokens, response)


@auth_router.post("/refresh")
async def refresh(
    service: AuthServiceDep,
    response: Response,
    refresh_token: Annotated[str | None, Cookie()] = None,
) -> AccessToken:
    try:
        tokens = await service.refresh_token(refresh_token)
    except InvalidRefreshToken as err:
        raise HTTPException(status_code=err.status_code, detail=err.message) from err

    return build_token_response(tokens, response)


@auth_router.post("/logout")
async def logout(
    service: AuthServiceDep,
    response: Response,
    refresh_token: Annotated[str | None, Cookie()] = None,
) -> None:
    try:
        await service.logout(refresh_token)
    except InvalidRefreshToken as err:
        raise HTTPException(status_code=err.status_code, detail=err.message) from err

    response.delete_cookie(
        "refresh_token",
        path=f"{settings.api_v1_prefix}{settings.api_v1_auth_prefix}",
    )


@auth_router.get("/me")
def me(current_user: CurrentUser) -> UserRead:
    return current_user
