import asyncio
import uuid

from pydantic import EmailStr

from app.auth.exceptions import InvalidCredentials
from app.auth.schemas import AccessToken, Tokens
from app.core.security import get_jwt_helper, get_password_helper
from app.users.service import UserService


class AuthService:
    def __init__(self, users: UserService) -> None:
        self.users = users
        self.pwd = get_password_helper()
        self.jwt = get_jwt_helper()

    async def login(self, email: EmailStr, password: str) -> Tokens:
        user = await self.users.get_user_by_email(email)
        hashed_password = user.password if user else None
        valid_password = await asyncio.to_thread(
            self.pwd.verify_password, password, hashed_password
        )
        if not user or not valid_password:
            raise InvalidCredentials()

        return self._issue_tokens(user.id)

    def _issue_tokens(self, user_id: uuid.UUID) -> Tokens:
        access_token = AccessToken(token=self.jwt.create_access_token(user_id))
        return Tokens(
            access_token=access_token, refresh_token=self.jwt.create_refresh_token()
        )
