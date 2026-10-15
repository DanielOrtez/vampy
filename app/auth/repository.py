import uuid
from datetime import UTC, datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import RefreshToken
from app.core.common.repository import BaseRepository


class AuthRepository(BaseRepository[RefreshToken]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_hash(self, token_hash: str) -> RefreshToken | None:
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

    async def revoke_refresh_token(self, token_id: uuid.UUID) -> bool:
        stmt = (
            update(RefreshToken)
            .where(RefreshToken.id == token_id)
            .where(RefreshToken.revoked_at.is_(None))
            .values(revoked_at=datetime.now(UTC))
            .returning(RefreshToken.id)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none() is not None

    async def revoke_refresh_token_family(self, family_id: uuid.UUID) -> None:
        stmt = (
            update(RefreshToken)
            .where(RefreshToken.family_id == family_id)
            .where(RefreshToken.revoked_at.is_(None))
            .values(revoked_at=datetime.now(UTC))
        )
        await self.session.execute(stmt)
        await self.session.commit()
