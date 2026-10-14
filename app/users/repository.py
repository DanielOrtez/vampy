from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.common.repository import BaseRepository
from app.users.models import User


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)

    async def get_by_email(self, email: EmailStr) -> User | None:
        stmt = select(User).where(User.email == email)
        return await self.session.scalar(stmt)
