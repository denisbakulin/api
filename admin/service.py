from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import EntityBadRequestError
from core.repository import BaseRepository
from core.service import BaseService
from user.service import UserService


class AdminService[T](BaseService[T, BaseRepository]):
    def __init__(self, model: T, session: AsyncSession):
        super().__init__(model, session)


    async def get_items_count(self) -> int:
        return await self.repository.get_items_count()



from user.model import User, UserRoleEnum
from user.schemas import UserCreate


class AdminUserService(UserService):

    async def create_super_admin(self, admin_data: UserCreate) -> User | None:
        admin = await self.repository.get_one_by(role=UserRoleEnum.SUPER_ADMIN)

        if admin:
            return admin

        admin = await self.create_user(
            user_data=admin_data
        )

        return await self.update_item(admin, role=UserRoleEnum.SUPER_ADMIN)

    async def create_anon(self, anon_data: UserCreate) -> User:

        anon = await self.repository.get_one_by(role=UserRoleEnum.ANONYMOUS)

        if anon:
            return anon

        anon = await self.create_user(
            user_data=anon_data
        )

        return await self.update_item(anon, role=UserRoleEnum.ANONYMOUS)


    async def edit_user_role(
            self,
            current: User,
            user: User,
            role: UserRoleEnum
    ) -> User:
        if user.role in (UserRoleEnum.SUPER_ADMIN, UserRoleEnum.ANONYMOUS):
            raise EntityBadRequestError(
                "Права",
                f"Нельзя посенять права пользователя {user.username}"
            )
        if current.role == UserRoleEnum.SUPER_ADMIN:
            if role not in (UserRoleEnum.SUPER_ADMIN, UserRoleEnum.ANONYMOUS):
                return await self.update_item(user, role=role)
            raise EntityBadRequestError(
                "Права",
                f"Нельзя создать пользователя с правами {role}"
            )
        if role in (UserRoleEnum.MODERATOR, UserRoleEnum.USER):
            return await self.update_item(user, role=role)
        raise EntityBadRequestError("Права", "Недостаточно прав!")









