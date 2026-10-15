from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.auth.dependency import AuthServiceDep
from app.auth.exceptions import InvalidCredentials
from app.auth.schemas import AccessToken
from app.core.config import get_settings

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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=err.detail)

    response.set_cookie(
        "vam:refresh_token",
        tokens.refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
    )
    return tokens.access_token


@auth_router.get("/me")
async def me(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    return token
