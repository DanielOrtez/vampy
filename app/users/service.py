import asyncio
import uuid

from pydantic import EmailStr

from app.core.security import get_password_helper
from app.users.exceptions import EmailAlreadyExistsError, UserNotFoundError
from app.users.models import User
from app.users.repository import UserRepository
from app.users.schemas import UserCreate


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository
        self.hasher = get_password_helper()

    async def get_user(self, id: uuid.UUID) -> User:
        user = await self.repository.get_by_id(id)
        if not user:
            raise UserNotFoundError(user_id=id)
        return user

    async def get_user_by_email(self, email: EmailStr) -> User | None:
        user = await self.repository.get_by_email(email)

        return user

    async def create_user(self, data: UserCreate) -> User:
        exists = await self.repository.get_by_email(data.email)
        if exists:
            raise EmailAlreadyExistsError()

        hashed_password = await asyncio.to_thread(
            self.hasher.hash_password, data.password
        )
        data.password = hashed_password
        user = await self.repository.create_user(data)

        return user
