from typing import Optional

from pydantic import BaseModel


class AccessTokenResponse(BaseModel):
    access_token: str


class LoginTokens(BaseModel):
    access_token: str
    refresh_token: str


class TokenInfo(BaseModel):
    type: str
    user_id: int


class AuthCreds(BaseModel):
    username: str = "admin"
    password: str = "admin"

