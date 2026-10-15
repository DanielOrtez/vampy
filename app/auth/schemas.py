from typing import Literal

from pydantic import BaseModel


class AccessToken(BaseModel):
    access_token: str
    expires_in: int
    token_type: Literal["Bearer"] = "Bearer"


class Tokens(BaseModel):
    access_token: AccessToken
    refresh_token: str
