from sqlalchemy.ext.asyncio import AsyncSession

from core.service import BaseService
from direct.service import DirectChatService
from user.model import User
from user.repository import UserRepository
from user.schemas import UserCreate
from user.utils import (UserSearchParams, generate_hashed_password)


class UserService(BaseService[User, UserRepository]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session, UserRepository)
        self.direct_service = DirectChatService(session)


    async def create_user(self, user_create: UserCreate) -> User:
        await self.check_already_exists(username=user_create.username)

        hashed_password = generate_hashed_password(password=user_create.password)

        user_create.password = hashed_password

        user = self.repository.create(
            **user_create.model_dump(),
        )

        await self.direct_service.create_favorites_chat(user)

        return user

    async def get_user_by_id(self, user_id: int) -> User:
        return await self.get_item_by_id(user_id)

    async def get_user_by_username(self, username: str) -> User:
        return await self.get_item_by(username=username)


    async def search_users(self, search: UserSearchParams) -> list[User]:

        return await self.search_items(
            search
        )







