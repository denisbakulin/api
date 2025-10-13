class AppError(Exception):
    """Базовая ошибка приложения"""


class EntityNotFoundError(AppError):
    """Ресурс не найден"""

    def __init__(
            self,
            entity: str,
            **fields
    ):
        super().__init__(
            f"{entity} "
            f"{f'с {", ".join(f"{k}={v}" for k, v in fields.items())} ' if fields else ''}"
            "не найдено!"
        )

        self.entity = entity



class EntityBadRequestError(AppError):
    """Ошибка создания/изменения ресурса"""

    def __init__(
            self,
            entity: str,
            message: str = ""
    ):
        super().__init__(
            f"[{entity}] Ошибка доступа к ресурсу"
            f" | {message}"
        )

        self.entity = entity


class EntityAlreadyExists(AppError):
    """Ресурс уже существует"""

    def __init__(self, entity: str, **fields):
        super().__init__(
            f"{entity} "
            f"{f'с {", ".join(f"{k}={v}" for k, v in fields.items())} ' if fields else ''}"
            "уже существует!"
        )
        self.entity = entity
        self.fields = fields


class EntityLockedError(AppError):
    """Ресурс заблокирован"""

    def __init__(self, entity: str | None = None, message: str | None = None):

        super().__init__(f"Ресурс [{entity}] заблокирован!" if not message else entity)
        self.entity = entity










