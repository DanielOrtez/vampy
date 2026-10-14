from fastapi import APIRouter

from app.users.router import users_router

main_router = APIRouter(prefix="/api/v1")

main_router.include_router(users_router)
