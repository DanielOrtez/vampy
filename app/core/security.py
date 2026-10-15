import hashlib
import uuid
from datetime import UTC, datetime, timedelta
from functools import cache
from secrets import token_urlsafe

import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

from app.core.config import get_settings


class PasswordHelper:
    def __init__(self) -> None:
        self.hasher = PasswordHash([Argon2Hasher()])
        self.fake_hash = self.hasher.hash(token_urlsafe(16))

    def hash_password(self, password: str) -> str:
        return self.hasher.hash(password)

    def verify_password(
        self, password: str, hashed_password: str | None = None
    ) -> bool:
        return self.hasher.verify(password, hashed_password or self.fake_hash)


class JWTHelper:
    def __init__(self):
        self.settings = get_settings()

    def create_access_token(self, user_id: uuid.UUID) -> str:
        now = datetime.now(UTC)
        payload = {
            "sub": str(user_id),
            "iat": now,
            "exp": now + timedelta(minutes=self.settings.access_token_minutes),
        }
        return jwt.encode(
            payload, self.settings.secret_key, algorithm=self.settings.algorithm
        )

    def decode_access_token(self, token: str) -> dict:
        return jwt.decode(
            token,
            self.settings.secret_key,
            [self.settings.algorithm],
            leeway=self.settings.leeway_seconds,
        )

    def create_refresh_token(self) -> str:
        return token_urlsafe(32)

    def hash_refresh_token(self, token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()


@cache
def get_password_helper() -> PasswordHelper:
    return PasswordHelper()
