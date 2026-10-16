import uuid

from pydantic import EmailStr

from app.core.exceptions import VAMException


class UserNotFoundError(VAMException):
    status_code: int = 409
    error: str = "user_not_found"

    def __init__(self, user_id: uuid.UUID | EmailStr):
        self.detail = {"user_id": f"User '{user_id}' not found."}


class EmailAlreadyExistsError(VAMException):
    status_code: int = 409
    error: str = "email_already_exists"

    def __init__(self):
        self.detail = {"email": "Email already exists."}
