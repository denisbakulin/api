import asyncio
from functools import wraps

from fastapi import HTTPException
from httpx import HTTPStatusError, RequestError

from integrations.exceptions import ExternalApiRequestError


class ExternalAPI:
    """Класс-родитель для создания внешних API"""

    def __init__(self, path: str, api_key: str = None):
        self.path = path
        self.api_key = api_key


def safe_request(func):
    """Декоратор для отлова дефолтных ошибок httpx"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"API error: {e}")
        except RequestError as e:
            raise HTTPException(status_code=502, detail=f"Ошибка соединения: {e}")
        except ExternalApiRequestError as e:
            raise HTTPException(status_code=400, detail=e.data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Неожиданная ошибка: {e}")
    return wrapper

async def main() -> None:
    ...


if __name__ == "__main__":
    asyncio.run(main())

