from typing import Annotated

from fastapi import Depends

from app.auth.service import AuthService
from app.users.dependency import get_user_service
from app.users.service import UserService


def get_auth_service(users: Annotated[UserService, Depends(get_user_service)]):
    return AuthService(users)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
