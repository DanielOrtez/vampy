from fastapi import APIRouter, HTTPException, status

from app.users.dependency import UserServiceDep
from app.users.exceptions import EmailAlreadyExistsError
from app.users.schemas import UserCreate, UserRead

users_router = APIRouter(tags=["users"], prefix="/users")


@users_router.post("")
async def create_user(data: UserCreate, service: UserServiceDep) -> UserRead:
    try:
        user = await service.create_user(data)
    except EmailAlreadyExistsError as err:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=err.detail
        ) from err

    return UserRead.model_validate(user)
