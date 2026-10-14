from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.dependency import AuthServiceDep
from app.auth.exceptions import InvalidCredentials
from app.auth.schemas import AccessToken

auth_router = APIRouter(tags=["auth"], prefix="/auth")


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
