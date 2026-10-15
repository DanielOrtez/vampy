from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.common.repository import BaseRepository
from app.users.models import User
from app.users.schemas import UserCreate


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)

    async def create_user(self, data: UserCreate) -> User:
        user = User(email=data.email, password=data.password)
        return await self.create(user)

    async def get_by_email(self, email: EmailStr) -> User | None:
        stmt = select(User).where(User.email == email)
        return await self.session.scalar(stmt)
