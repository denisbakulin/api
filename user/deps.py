from typing import Annotated

from fastapi import Depends

from core.db import getSessionDep
from user.model import User, UserRoleEnum
from user.service import UserService


def get_user_service(
        session: getSessionDep
) -> UserService:
    return UserService(session=session)


userServiceDep = Annotated[UserService, Depends(get_user_service)]


async def get_user(
        user_service: userServiceDep,
        username: str
) -> User:
    return await user_service.get_user_by_username(username)


async def get_anon(
        user_service: userServiceDep
) -> User:
    return await user_service.get_item_by(role=UserRoleEnum.ANONYMOUS)


anonDep = Annotated[User, Depends(get_anon)]
userDep = Annotated[User, Depends(get_user)]

