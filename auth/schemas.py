from pydantic import BaseModel
from typing import Optional


class AccessTokenResponse(BaseModel):
    access_token: str


class LoginTokens(BaseModel):
    access_token: str
    refresh_token: str


class TokenInfo(BaseModel):
    type: str
    user_id: int


class AuthCreds(BaseModel):
    username: str
    password: str


class TelegramUser(BaseModel):
    id: int
    is_bot: Optional[bool] = False
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    allows_write_to_pm: Optional[bool] = None


class TelegramAuth(BaseModel):
    initData: str

