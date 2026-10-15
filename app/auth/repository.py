import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import RefreshToken
from app.core.common.repository import BaseRepository


class AuthRepository(BaseRepository[RefreshToken]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_hash(self, token_hash: str):
        stmt = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        return await self.session.scalar(stmt)

    async def add_refresh_token(
        self,
        user_id: uuid.UUID,
        token_hash: str,
        expires_at: datetime,
        family_id: uuid.UUID | None = None,
    ) -> str:
        token = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        if family_id:
            token.family_id = family_id
        refresh_token = await self.create(token)
        return refresh_token.token_hash
