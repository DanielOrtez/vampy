from typing import Annotated

from fastapi import Depends

from app.core.database import AsyncSessionDep
from app.users.repository import UserRepository
from app.users.service import UserService


def get_user_repository(session: AsyncSessionDep):
    return UserRepository(session)


def get_user_service(
    repository: Annotated[UserRepository, Depends(get_user_repository)],
):
    return UserService(repository)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
