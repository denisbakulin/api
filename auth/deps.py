from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from auth.exceptions import InvalidTokenError
from auth.schemas import TokenInfo
from auth.service import AuthService
from auth.utils import decode_token
from core.db import get_session
from core.exceptions import EntityLockedError
from user.deps import get_user_service
from user.model import User
from user.service import UserService
from user.model import UserRoleEnum
from typing import Callable
from operator import ge

Operator = Callable[[UserRoleEnum, UserRoleEnum], bool]
security = HTTPBearer()

async def get_user_token(
        creds: HTTPAuthorizationCredentials = Depends(security),
) -> TokenInfo:
    if creds.scheme != "Bearer":
        raise InvalidTokenError(
            f"Invalid auth schema: {creds.scheme} (Bearer need)"
        )
    token = creds.credentials

    return decode_token(token)


async def get_current_user(
    token: TokenInfo = Depends(get_user_token),
    user_service: UserService = Depends(get_user_service)
) -> User:
    user = await user_service.get_user_by_id(token.user_id)

    if user.is_active:
        return user

    raise EntityLockedError(
        message=f"Пользователь {user.username} временно заблокирован"
    )



def role_validate(role: UserRoleEnum, operator: Operator = ge):
    """Проверяет права пользователя"""

    async def wrapper(user: User = Depends(get_current_user)):
        if operator(user.role, role):
            return user
        raise HTTPException(detail="Недостаточно прав", status_code=403)
    return wrapper


async def get_auth_service(
        session: AsyncSession = Depends(get_session)
) -> AuthService:
    return AuthService(session=session)


currentUserDep = Annotated[User, Depends(get_current_user)]
authServiceDep = Annotated[AuthService, Depends(get_auth_service)]