from fastapi import status
from fastapi import status as st
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from auth.exceptions import AuthError
from core.exceptions import (EntityAlreadyExists, EntityBadRequestError,
                             EntityLockedError, EntityNotFoundError, AppError)


class ErrorResponse(JSONResponse):

    def __init__(self, status_code: status, exc: Exception):
        super().__init__(status_code=status_code, content={"detail": str(exc)})

class AppExceptionMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        try:
            return await call_next(request)

        except EntityNotFoundError as exc:
            return ErrorResponse(status.HTTP_404_NOT_FOUND, exc)

        except EntityAlreadyExists as exc:
            return ErrorResponse(status.HTTP_403_FORBIDDEN, exc)

        except EntityBadRequestError as exc:
            return ErrorResponse(status.HTTP_422_UNPROCESSABLE_ENTITY, exc)

        except AuthError as exc:
            return ErrorResponse(status.HTTP_401_UNAUTHORIZED, exc)

        except EntityLockedError as exc:
            return ErrorResponse(status.HTTP_423_LOCKED, exc)




