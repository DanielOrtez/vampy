import asyncio
import uuid

from pydantic import EmailStr

from app.core.security import get_password_helper
from app.users.exceptions import EmailAlreadyExistsError, UserNotFoundError
from app.users.repository import UserRepository
from app.users.schemas import UserCreate, UserPrivate, UserRead


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository
        self.hasher = get_password_helper()

    async def get_user(self, id: uuid.UUID) -> UserRead:
        user = await self.repository.get_by_id(id)
        if not user:
            raise UserNotFoundError(user_id=id)
        return UserRead.model_validate(user)

    async def get_user_by_email(self, email: EmailStr) -> UserPrivate | None:
        user = await self.repository.get_by_email(email)

        return UserPrivate.model_validate(user) if user else None

    async def create_user(self, data: UserCreate) -> UserRead:
        exists = await self.repository.get_by_email(data.email)
        if exists:
            raise EmailAlreadyExistsError()

        hashed_password = await asyncio.to_thread(
            self.hasher.hash_password, data.password
        )
        data.password = hashed_password
        user = await self.repository.create_user(data)

        return UserRead.model_validate(user)
