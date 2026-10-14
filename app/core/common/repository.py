import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base


class BaseRepository[ModelType: Base]:
    def __init__(self, model: type[ModelType], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get_by_id(self, id: int | uuid.UUID) -> ModelType | None:
        return await self.session.get(self.model, id)

    async def get_all(self, offset: int = 0, limit: int = 50) -> Sequence[ModelType]:
        stmt = select(self.model).offset(offset).limit(limit)
        result = await self.session.scalars(stmt)
        return result.all()

    async def create(self, obj: ModelType) -> ModelType:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj: ModelType) -> None:
        return await self.session.delete(obj)
