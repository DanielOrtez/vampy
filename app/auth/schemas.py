import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class AccessToken(BaseModel):
    access_token: str
    expires_in: int
    token_type: Literal["Bearer"] = "Bearer"


class DecodedToken(BaseModel):
    sub: uuid.UUID
    iat: datetime
    exp: datetime


class Tokens(BaseModel):
    access_token: AccessToken
    refresh_token: str
