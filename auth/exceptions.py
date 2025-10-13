from core.exceptions import AppError


class AuthError(AppError):
    """Ошибка аутентификации"""

class InvalidTokenError(AuthError):
    """Ошибка JWT"""


class TelegramAuthError(AuthError):
    """Ошибка входа через telegram"""


class InvalidPasswordError(AuthError):
    """Ошибка некорректного пароля"""

    def __init__(self, message: str | None = None):
        if message is None:
            message = "Некорректный пароль"
        super().__init__(message)
