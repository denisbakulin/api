from admin.views.base import AdminView

from user.model import User, UserRoleEnum
from user.schemas import UserShowMe, UserCreate
from user.deps import userServiceDep, userDep
from auth.deps import currentUserDep
from admin.schemas import AdminUserUpdate
from admin.deps import adminUserServiceDep

class UserAdminView(AdminView, model=User):
    show = UserShowMe

    def init_custom_views(self):

        @self.post(
            "",
            summary="Создать пользователя",
            response_model=self.show
        )
        async def create_user(
                user_service: userServiceDep,
                user_create: UserCreate,
        ):
            return await user_service.create_user(user_create)

        @self.patch(
            "/{username}",
            summary="Изменить пользователя",
            response_model=self.show
        )
        async def update_user(
                user: userDep,
                user_data: AdminUserUpdate,
                user_service: userServiceDep
        ):
            return await user_service.update_user(user, user_data)

        @self.put(
            "/{username}/role",
            summary="",
            response_model=self.show,
        )
        async def add_edit_role(
                user: userDep,
                admin: currentUserDep,
                user_service: adminUserServiceDep,
                role: UserRoleEnum

        ):
            return await user_service.edit_user_role(admin, user, role=role)