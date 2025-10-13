from enum import StrEnum

from fastapi import Response
from jose import JWTError, jwt

from auth.exceptions import InvalidTokenError
from auth.schemas import TokenInfo
from core.settings import jwt_auth_settings, tg_auth_settings

from datetime import datetime, timedelta

import hashlib
import hmac
from urllib.parse import parse_qsl

from auth.exceptions import TelegramAuthError
from auth.schemas import TelegramUser

class TokenTypes(StrEnum):
    access = "access"
    refresh = "refresh"




class TokenCreator:
    """Класс-генератор JWT токенов по user_id"""
    def __init__(self, user_id: int):
        self.user_id = user_id

    def _create_token(
            self,
            token_type: TokenTypes,
            age: timedelta
    ) -> str:
        expire = datetime.now() + age
        payload = {"sub": str(self.user_id), "exp": expire, "type": token_type}
        return jwt.encode(payload, jwt_auth_settings.secret_key, jwt_auth_settings.algorithm)

    @property
    def access(self) -> str:
        age = timedelta(minutes=jwt_auth_settings.access_token_expire_minutes)
        return self._create_token(TokenTypes.access, age)

    @property
    def refresh(self) -> str:
        age = timedelta(days=jwt_auth_settings.refresh_token_expire_days)
        return self._create_token(TokenTypes.refresh, age)



def decode_token(token: str) -> TokenInfo:
    """Декодирует JWT токен из SHA256"""

    try:
        payload = jwt.decode(
            token,
            jwt_auth_settings.secret_key,
            algorithms=[jwt_auth_settings.algorithm]
        )

        user_id = int(payload["sub"])
        token_type = payload["type"]

        return TokenInfo(user_id=user_id, type=token_type)
    except JWTError:
        raise InvalidTokenError("Невалидный или истекший токен")


def set_refresh_token_cookie(response: Response, token):
    response.set_cookie(
        key="refresh_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
        path="/"
    )

def check_telegram_auth(data: str) -> TelegramUser:
    parsed = dict(parse_qsl(data))
    hash_ = parsed.pop("hash", None)

    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))
    secret_key = hashlib.sha256(tg_auth_settings.token.encode()).digest()
    calc_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if calc_hash != hash_:
        raise TelegramAuthError("Некорректный токен авторизации initData")

    return TelegramUser.model_validate(parsed.get("user"))


