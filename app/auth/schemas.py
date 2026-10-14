from typing import Literal

from pydantic import BaseModel


class AccessToken(BaseModel):
    token: str
    token_type: Literal["bearer"] = "bearer"


class Tokens(BaseModel):
    access_token: AccessToken
    refresh_token: str
