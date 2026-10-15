from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.auth.dependency import AuthServiceDep, CurrentUser
from app.auth.exceptions import InvalidCredentials, InvalidRefreshToken
from app.auth.schemas import AccessToken
from app.core.config import get_settings
from app.users.schemas import UserRead

auth_router = APIRouter(tags=["auth"], prefix="/auth")

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_v1_prefix}/auth/login")


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
    return service.build_response(tokens, response)


@auth_router.post("/refresh")
async def refresh(
    refresh_token: Annotated[str, Cookie()], service: AuthServiceDep, response: Response
) -> AccessToken:
    try:
        tokens = await service.refresh_token(refresh_token)
    except InvalidRefreshToken as err:
        raise HTTPException(status_code=err.status_code, detail=err.message) from err

    return service.build_response(tokens, response)


@auth_router.get("/me")
def me(current_user: CurrentUser) -> UserRead:
    return current_user
