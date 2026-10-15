import asyncio
import uuid
from datetime import UTC, datetime, timedelta

from jwt import PyJWTError
from pydantic import EmailStr

from app.auth.exceptions import (
    InvalidAccessToken,
    InvalidCredentials,
    InvalidRefreshToken,
)
from app.auth.models import RefreshToken
from app.auth.repository import AuthRepository
from app.auth.schemas import AccessToken, Tokens
from app.core.config import get_settings
from app.core.security import JWTHelper, get_password_helper
from app.users.schemas import UserRead
from app.users.service import UserService


class AuthService:
    def __init__(self, users: UserService, repository: AuthRepository) -> None:
        self.users = users
        self.repository = repository
        self.pwd = get_password_helper()
        self.jwt = JWTHelper()
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

    async def authenticate(self, token: str) -> UserRead:
        try:
            decoded = self.jwt.decode_access_token(token)
        except PyJWTError:
            raise InvalidAccessToken()

        user = await self.users.get_user(decoded.sub)
        if not user:
            raise InvalidAccessToken()

        return user

    async def logout(self, refresh_token: str | None = None) -> None:
        token = await self._manage_refresh(refresh_token)

        await self.repository.revoke_refresh_token_family(token.family_id)

    async def refresh_token(self, refresh_token: str | None = None) -> Tokens:
        token = await self._manage_refresh(refresh_token)
        valid = await self.repository.revoke_refresh_token(token.id)

        if not valid:
            await self.repository.revoke_refresh_token_family(token.family_id)
            raise InvalidRefreshToken()

        return await self._issue_tokens(
            user_id=token.user_id, family_id=token.family_id
        )

    async def _manage_refresh(self, refresh_token: str | None = None) -> RefreshToken:
        if not refresh_token:
            raise InvalidRefreshToken()

        token = await self.repository.get_by_hash(
            self.jwt.hash_refresh_token(refresh_token)
        )
        if not token or token.expires_at < datetime.now(UTC):
            raise InvalidRefreshToken()

        return token

    async def _issue_tokens(
        self, user_id: uuid.UUID, family_id: uuid.UUID | None = None
    ) -> Tokens:
        access_token = AccessToken(
            access_token=self.jwt.create_access_token(user_id),
            expires_in=self.settings.access_token_minutes * 60,
        )
        refresh_token = self.jwt.create_refresh_token()
        expires_at = datetime.now(UTC) + timedelta(
            days=self.settings.refresh_token_days
        )
        await self.repository.add_refresh_token(
            user_id=user_id,
            token_hash=self.jwt.hash_refresh_token(refresh_token),
            expires_at=expires_at,
            family_id=family_id,
        )
        return Tokens(access_token=access_token, refresh_token=refresh_token)
