from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.auth.exceptions import InvalidAccessToken, InvalidCredentials
from app.auth.repository import AuthRepository
from app.auth.service import AuthService
from app.core.config import get_settings
from app.core.database import AsyncSessionDep
from app.users.dependency import get_user_service
from app.users.schemas import UserRead
from app.users.service import UserService

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.api_v1_prefix}/{settings.api_v1_auth_prefix}/login"
)


def get_auth_service(
    users: Annotated[UserService, Depends(get_user_service)], session: AsyncSessionDep
) -> AuthService:
    return AuthService(users, AuthRepository(session))


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], service: AuthServiceDep
) -> UserRead:
    try:
        return await service.authenticate(token)
    except (InvalidCredentials, InvalidAccessToken) as err:
        raise HTTPException(status_code=err.status_code, detail=err.message) from err


CurrentUser = Annotated[UserRead, Depends(get_current_user)]
