from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from admin.service import AdminService
from core.db import getSessionDep


def get_admin_service(
        model,
) -> Callable[[AsyncSession], AdminService]:
    def wrapper(session: getSessionDep):
        return AdminService[model](model=model, session=session)
    return wrapper


from typing import Annotated

from fastapi import Depends

from admin.service import AdminUserService


async def get_admin_user_service(
        session: getSessionDep
) -> AdminUserService:
    return AdminUserService(session=session)

adminUserServiceDep = Annotated[AdminUserService, Depends(get_admin_user_service)]







