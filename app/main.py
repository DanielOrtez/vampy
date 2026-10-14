from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from sqlalchemy import text

from app.core import database
from app.core.config import get_settings
from app.core.database import AsyncSessionDep


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    yield

    await database.dispose_engine()


def create_app() -> FastAPI:
    settings = get_settings()

    api = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
        openapi_url="/openapi.json" if not settings.is_production else None,
    )

    api.add_middleware(GZipMiddleware, minimum_size=1000)

    if settings.allowed_hosts:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(host) for host in settings.allowed_hosts],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @api.get("/ready")
    async def read_root(session: AsyncSessionDep):
        await session.execute(text("SELECT 1"))
        return {"status": "ready!"}

    return api


app = create_app()
