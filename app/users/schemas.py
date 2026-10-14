import uuid

from pydantic import BaseModel, EmailStr

from app.core.common.schemas import ResponseSchema


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserRead(ResponseSchema):
    id: uuid.UUID
    email: EmailStr
