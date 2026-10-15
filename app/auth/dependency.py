from typing import Annotated

from fastapi import Depends

from app.auth.repository import AuthRepository
from app.auth.service import AuthService
from app.core.database import AsyncSessionDep
from app.users.dependency import get_user_service
from app.users.service import UserService


def get_auth_service(
    users: Annotated[UserService, Depends(get_user_service)], session: AsyncSessionDep
):
    return AuthService(users, AuthRepository(session))


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
