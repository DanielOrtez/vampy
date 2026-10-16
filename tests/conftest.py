from collections.abc import AsyncGenerator

import pytest
from httpx2 import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings
from app.core.database import Base, get_async_session
from app.core.security import get_password_helper
from app.main import app
from app.users.models import User

TEST_USER_PASSWORD = "test123456@"

settings = get_settings()
db_url = f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/test"


@pytest.fixture(autouse=True)
async def engine() -> AsyncGenerator[AsyncEngine]:
    engine = create_async_engine(db_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession]:
    session_maker = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with session_maker() as session:
        try:
            yield session
        finally:
            await session.rollback()


@pytest.fixture
async def client(session: AsyncSession) -> AsyncGenerator[AsyncClient]:
    async def override_get_db():
        yield session

    app.dependency_overrides[get_async_session] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
async def user(session: AsyncSession) -> User:
    user = User(
        email="test@test.com",
        password=get_password_helper().hash_password(TEST_USER_PASSWORD),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    user.plain_password = TEST_USER_PASSWORD  # ty: ignore
    return user
