from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from admin.schemas import AdminUserUpdate
from auth.exceptions import InvalidPasswordError
from core.exceptions import EntityAlreadyExists, EntityBadRequestError
from core.service import BaseService
from helpers.search import Pagination
from user.model import Profile, User, Settings
from user.repository import UserRepository
from user.schemas import UserCreate, UserUpdate, PasswordCreate,UserSettings
from user.utils import (UserSearchParams, generate_hashed_password,
                        verify_password)
from direct.service import DirectChatService
from uuid import uuid4

from auth.schemas import TelegramUser


class UserService(BaseService[User, UserRepository]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session, UserRepository)
        self.direct_chat_service = DirectChatService(session)
        self.base_serv = BaseService(Profile, session)



    async def create_user(self, user_data: UserCreate, is_admin=False) -> User:
        await self.check_already_exists(username=user_data.username)
        await self.check_already_exists(email=user_data.email)

        hashed_password = generate_hashed_password(password=user_data.password)

        user_data.password = hashed_password

        user = self.repository.create_user(
            **user_data.model_dump(),
            is_admin=is_admin
        )

        await self.direct_chat_service.create_favorites_chat(user)

        return user

    async def login_user_via_telegram(self, tg_user: TelegramUser) -> User:
        user = await self.repository.get_user(tg_id=tg_user.id)

        if user is not None:
            return user

        user_exists = await self.repository.exists(username=tg_user.username)

        if user_exists:
            tg_user.username = str(uuid4().hex[:10])

        user = await self.create_item(
            tg_id=tg_user.id,
            username=tg_user.username,
        )

        return user



    async def get_user_by_id(self, user_id: int) -> User:
        return await self.get_item_by_id(user_id)


    async def get_user_by_username(self, username: str) -> User:
        return await self.get_item_by(username=username)


    async def create_first_admin(self, admin_data: UserCreate) -> Optional[User]:

        admin = await self.repository.exists(is_admin=True)

        if admin:
            return

        return await self.create_user(
            user_data=admin_data,
            is_admin=True,
        )


    async def update_user(self, user: User, update_info: UserUpdate | AdminUserUpdate ) -> User:
        if update_info.username:

            user_existing = await self.repository.get_user(username=update_info.username)

            if user_existing and user_existing.id != user.id:
                raise EntityAlreadyExists(
                    entity="User",
                    field="username",
                    value=update_info.username
                )
            await self.update_item(user, username=update_info.username)

        if update_info.email:
            user_existing = await self.repository.get_user(email=update_info.email)

            if user_existing and user_existing.id != user.id:
                raise EntityAlreadyExists(
                    entity="User",
                    field="email",
                    value=update_info.email
                )

        await self.base_serv.update_item(user.profile, **update_info.profile.model_dump(exclude_none=True))

        return user


    async def change_password(self, user: User, old_password, new_password):
        if not verify_password(old_password, user.password):
            raise InvalidPasswordError()

        password = generate_hashed_password(new_password)

        await self.update_item(user, password=password)

    async def set_password(self, user: User, pwd: PasswordCreate) -> User:
        if user.password_login:
            raise EntityBadRequestError("Пароль", "Пароль уже установлен")

        return await self.update_item(user, password=pwd.password)

    async def search_users(self, search: UserSearchParams, pagination: Pagination) -> list[User]:
        return await self.search_items(
            search, pagination,
            inner_props={
                "settings.show_in_search": True
            }
        )

    async def edit_user_settings(self, user: User, settings: UserSettings) -> Settings:

        await self.update_item(user.settings, **settings.dict())

        return user.settings








