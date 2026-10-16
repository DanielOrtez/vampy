from fastapi import APIRouter

from app.users.dependency import UserServiceDep
from app.users.schemas import UserCreate, UserRead

users_router = APIRouter(tags=["users"], prefix="/users")


@users_router.post("/signup")
async def create_user(data: UserCreate, service: UserServiceDep) -> UserRead:
    user = await service.create_user(data)

    return UserRead.model_validate(user)
