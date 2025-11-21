from sqlalchemy.ext.asyncio import AsyncSession
from core.exceptions import (EntityBadRequestError, EntityLockedError,
                             EntityNotFoundError)
from core.repository import BaseRepository
from core.service import BaseService
from direct.manager import WebSocketManager
from direct.model import DirectChat, DirectMessage, DirectUserSettings
from direct.repository import DirectChatRepository
from direct.schemas import (DirectChatShow, DirectUserSettingsSchema,
                            MessageCreate)

from user.model import User
from asyncio import gather


class DirectUserSettingsService(BaseService[DirectUserSettings, BaseRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(DirectUserSettings, session)


    async def init_settings(self, chat_id: int, user_id1: int, user_id2: int) -> None:

        tasks = [self.create_item(chat_id=chat_id, user_id=user_id)
                 for user_id in (user_id1, user_id2)]

        await gather(*tasks)


    async def get_users_settings(
            self,
            chat_id: int,
            recipient_id: int,
            sender_id: int
    ) -> tuple[DirectUserSettings, DirectUserSettings]:

        settings_partial = partial(
            self.get_item_by,
            chat_id=chat_id
        )

        recipient_settings = await settings_partial(
            user_id=recipient_id
        )

        sender_settings = await settings_partial(
            user_id=sender_id
        )

        return (recipient_settings, sender_settings)


class DirectMessageService(BaseService[DirectMessage, BaseRepository]):
    def __init__(self, session: AsyncSession):
        super().__init__(DirectMessage, session)

    async def get_messages(
            self,
            user: User,
            recipient: User,
    ) -> list[DirectMessage]:

        return await self.repository.get_any_by(
            sender_id=user.id, recipient_id=recipient.id
        )

from functools import partial

class DirectChatService(BaseService[DirectChat, DirectChatRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(DirectChat, session, DirectChatRepository)
        self.message_service = DirectMessageService(session)
        self.settings_service = DirectUserSettingsService(session)
        self.ws_manager = WebSocketManager()

    async def create_direct(
            self,
            user_1: User,
            user_2: User
    ) -> DirectChat:
        chat = await self.create_item(
            first_user_id=user_1.id, second_user_id=user_2.id
        )

        await self.settings_service.init_settings(
            chat_id=chat.id, user_id1=user_1.id, user_id2=user_2.id
        )

        return chat

    async def create_favorites_chat(self, user: User) -> DirectChat:
        await self.check_already_exists(first_user_id=user.id, second_user_id=user.id)

        chat = await self.create_item(
            first_user_id=user.id, second_user_id=user.id
        )

        await self.settings_service.create_item(
            chat_id=chat.id,
            user_id=user.id,
            chat_name="Избранное"
        )

        return chat


    async def create_message(
            self,
            sender: User,
            recipient: User,
            message_info: MessageCreate
    ) -> DirectMessage:

        chat = await self.repository.chat_exists(sender.id, recipient.id)

        if chat is None:
            await self.create_direct(sender, recipient)


        message = await self.message_service.create_item(
            sender_id=sender.id,
            recipient_id=recipient.id,
            content=message_info.content
        )

        await self.ws_manager.message_notify(
            recipient_id=recipient.id,
            message_id=message.id,
            message=message.content,
            username=sender.username
        )

        return message

    async def get_direct_settings(
            self, user: User, recipient: User
    ) -> DirectUserSettings:

        chat = await self.get_item_by(
            first_user_id=user.id, second_user_id=recipient.id
        )

        user_settings = await self.settings_service.get_item_by(
            chat_id=chat.id,
            user_id=recipient.id
        )

        return user_settings


    async def edit_direct_settings(
            self, current: User,
            recipient: User,
            settings: DirectUserSettingsSchema
    ) -> DirectUserSettings:

        if current.id == recipient.id:
            raise EntityBadRequestError("Избранное", "Невозможно изменить этот чат")

        user_settings = await self.get_direct_settings(current, recipient)

        await self.settings_service.update_item(
            user_settings, **settings.dict()
        )

        return user_settings


    async def get_user_chats(self, user: User) -> list[DirectChatShow]:

        result = await self.repository.get_user_chats(user_id=user.id)
        return [DirectChatShow(settings=settings, user=user) for settings, user in result]


    async def get_direct(self, user1: User, user2: User) -> DirectChat:
        direct = await self.repository.chat_exists(user1.id, user2.id)

        if direct:
            return direct

        raise EntityNotFoundError(
            "Личный чат",
            username1=user1.username,
            username2=user2.username
        )