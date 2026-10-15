import uuid

from pydantic import EmailStr

from app.core.common.schemas import BaseSchema


class UserEmailMixin:
    email: EmailStr


class UserCreate(UserEmailMixin, BaseSchema):
    password: str


class UserPrivate(UserEmailMixin, BaseSchema):
    id: uuid.UUID
    password: str


class UserRead(UserEmailMixin, BaseSchema):
    id: uuid.UUID
