from fastapi import status
from fastapi import status as st
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from auth.exceptions import AuthError
from core.exceptions import (EntityAlreadyExists, EntityBadRequestError,
                             EntityLockedError, EntityNotFoundError)


class AppExceptionMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        try:
            return await call_next(request)
        except EntityNotFoundError as exc:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": str(exc)}
            )
        except EntityAlreadyExists as exc:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": str(exc)}
            )

        except EntityBadRequestError as exc:
            return JSONResponse(
                status_code=st.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"detail": str(exc)}

            )
        except AuthError as exc:
            return JSONResponse(
                status_code=st.HTTP_401_UNAUTHORIZED,
                content={"detail": str(exc)}
            )
        except EntityLockedError as exc:
            return JSONResponse (
                status_code=st.HTTP_423_LOCKED,
                content={"detail" : str(exc)}
            )




