from datetime import datetime, timedelta
from enum import StrEnum

from fastapi import Response
from jose import JWTError, jwt

from auth.exceptions import InvalidTokenError
from auth.schemas import TokenInfo
from core.settings import AuthSettings


class TokenTypes(StrEnum):
    access = "access"
    pending_access = "pending_access"
    refresh = "refresh"
    verify = "verify"
    change_email = "change-email"


config = AuthSettings.get()


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
        return jwt.encode(payload, config.secret_key, config.algorithm)

    @property
    def access(self) -> str:
        age = timedelta(minutes=config.access_token_expire_minutes)
        return self._create_token(TokenTypes.access, age)

    @property
    def verify(self) -> str:
        age = timedelta(hours=config.verify_token_expire_hours)
        return self._create_token(TokenTypes.verify, age)

    @property
    def pending_access(self) -> str:
        age = timedelta(hours=config.verify_token_expire_hours)
        return self._create_token(TokenTypes.pending_access, age)

    @property
    def refresh(self) -> str:
        age = timedelta(days=config.refresh_token_expire_days)
        return self._create_token(TokenTypes.refresh, age)

    @property
    def change_email(self) -> str:
        age = timedelta(hours=config.verify_token_expire_hours)
        return self._create_token(TokenTypes.change_email, age)


def decode_token(token: str) -> TokenInfo:
    """Декодирует JWT токен из SHA256"""
    try:
        payload = jwt.decode(
            token,
            config.secret_key,
            algorithms=[config.algorithm]
        )

        user_id = int(payload["sub"])
        token_type = payload["type"]

        return TokenInfo(user_id=user_id, type=token_type)
    except JWTError:
        raise InvalidTokenError("Невалидный или истекший токен")


from datetime import datetime, timedelta


def set_refresh_token_cookie(response: Response, token):
    response.set_cookie(
        key="refresh_token",
        value=token,
        httponly=True,
        samesite="lax",  # или "strict" / "none" если фронтенд на другом домене
        max_age=60 * 60 * 24 * 7,  # 7 дней, или сколько нужно
        path="/"
    )

from urllib.parse import parse_qsl
import hashlib, hmac


BOT_TOKEN="7555036857:AAF51SdEQb8zQGMuGmxvjl9H2LND_oNiJ1w"


from auth.schemas import TelegramUser
from auth.exceptions import TelegramAuthError

def check_telegram_auth(data: str) -> TelegramUser:
    parsed = dict(parse_qsl(data))
    hash_ = parsed.pop("hash", None)

    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))
    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
    calc_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if calc_hash != hash_:
        raise TelegramAuthError("Некорректный токен авторизации initData")

    return TelegramUser.model_validate(parsed.get("user"))


