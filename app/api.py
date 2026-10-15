from fastapi import APIRouter

from app.auth.router import auth_router
from app.core.config import get_settings
from app.users.router import users_router

settings = get_settings()
main_router = APIRouter(prefix=settings.api_v1_prefix)

main_router.include_router(users_router)
main_router.include_router(auth_router)
