import asyncio
import uuid
from datetime import UTC, datetime, timedelta

from pydantic import EmailStr

from app.auth.exceptions import InvalidCredentials
from app.auth.repository import AuthRepository
from app.auth.schemas import AccessToken, Tokens
from app.core.config import get_settings
from app.core.security import get_jwt_helper, get_password_helper
from app.users.service import UserService


class AuthService:
    def __init__(self, users: UserService, repository: AuthRepository) -> None:
        self.users = users
        self.repository = repository
        self.pwd = get_password_helper()
        self.jwt = get_jwt_helper()
        self.settings = get_settings()

    async def login(self, email: EmailStr, password: str) -> Tokens:
        user = await self.users.get_user_by_email(email)
        hashed_password = user.password if user else None
        valid_password = await asyncio.to_thread(
            self.pwd.verify_password, password, hashed_password
        )
        if not user or not valid_password:
            raise InvalidCredentials()

        return await self._issue_tokens(user.id)

    async def _issue_tokens(self, user_id: uuid.UUID) -> Tokens:
        access_token = AccessToken(token=self.jwt.create_access_token(user_id))
        refresh_token = self.jwt.create_refresh_token()
        expires_at = datetime.now(UTC) + timedelta(
            days=self.settings.refresh_token_days
        )
        await self.repository.add_refresh_token(
            user_id=user_id,
            token_hash=self.jwt.hash_refresh_token(refresh_token),
            expires_at=expires_at,
        )
        return Tokens(access_token=access_token, refresh_token=refresh_token)
