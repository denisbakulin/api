from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from auth.exceptions import InvalidPasswordError
from auth.schemas import TelegramUser
from core.exceptions import EntityBadRequestError
from core.service import BaseService
from direct.service import DirectChatService
from helpers.search import Pagination
from user.model import Profile, Settings, User
from user.repository import UserRepository
from user.schemas import PasswordCreate, UserCreate, UserSettings, UserUpdate, PasswordChange
from user.utils import (UserSearchParams, generate_hashed_password,
                        verify_password)


class UserService(BaseService[User, UserRepository]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session, UserRepository)
        self.direct_service = DirectChatService(session)
        self.profile_service = BaseService(Profile, session)


    async def create_user(self, user_create: UserCreate) -> User:
        await self.check_already_exists(username=user_create.username)
        await self.check_already_exists(email=user_create.email)

        hashed_password = generate_hashed_password(password=user_create.password)

        user_create.password = hashed_password

        user = self.repository.create(
            **user_create.model_dump(),
        )

        await self.direct_service.create_favorites_chat(user)

        return user


    async def login_user_via_telegram(self, tg_user: TelegramUser) -> User:
        user = await self.repository.get_one_by(tg_id=tg_user.id)

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


    async def update_user(self, user: User, user_update: UserUpdate) -> User:
        await self.check_already_exists(username=user_update.username)
        await self.check_already_exists(email=user_update.email)

        user_data = user_update.model_dump(exclude_none=True)
        profile_data: dict | None = user_data.pop("profile", None)

        await self.update_item(user, **user_data)

        if profile_data is not None:
            await self.profile_service.update_item(
                user.profile, **profile_data
            )
        return user



    async def change_password(self, user: User, pwd: PasswordChange):
        if not verify_password(pwd.old_password, user.password):
            raise InvalidPasswordError()

        password = generate_hashed_password(pwd.new_password)

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








