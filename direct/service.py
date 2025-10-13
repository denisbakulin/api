from asyncio import gather

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
from helpers.search import Pagination
from user.model import User


class DirectUserSettingsService(BaseService[DirectUserSettings, BaseRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(DirectUserSettings, session)


class DirectMessageService(BaseService[DirectMessage, BaseRepository]):
    def __init__(self, session: AsyncSession):
        super().__init__(DirectMessage, session)

    async def get_messages(
            self,
            user: User,
            recipient: User,
            pagination: Pagination
    ) -> list[DirectMessage]:

        return await self.repository.get_any_by(
            sender_id=user.id, recipient_id=recipient.id, **pagination.get()
        )



class DirectChatService(BaseService[DirectChat, DirectChatRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(DirectChat, session, DirectChatRepository)
        self.message_service = DirectMessageService(session)
        self.direct_user_settings_service = DirectUserSettingsService(session)
        self.ws_manager = WebSocketManager()

    async def create_direct(
            self,
            user_1: User,
            user_2: User
    ) -> DirectChat:
        chat = await self.create_item(
            first_user_id=user_1.id, second_user_id=user_2.id
        )

        await self.direct_user_settings_service.create_item(
            chat_id=chat.id,
            user_id=user_1.id
        )
        await self.direct_user_settings_service.create_item(
            chat_id=chat.id,
            user_id=user_2.id,
        )

        return chat

    async def create_favorites_chat(self, user: User) -> DirectChat:
        await self.check_already_exists(first_user_id=user.id, second_user_id=user.id)

        chat = await self.create_item(
            first_user_id=user.id, second_user_id=user.id
        )

        await self.direct_user_settings_service.create_item(
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
        if not recipient.settings.enable_direct:
            raise EntityBadRequestError(
                message=f"Пользователь {recipient.username} не принимает сообщения"
            )

        chat = await self.repository.chat_exists(sender.id, recipient.id)

        if chat is None:
            chat = await self.create_direct(sender, recipient)

        if chat.banned_user_id is not None:
            raise EntityLockedError(f"Чат [{sender.username} - {recipient.username}]")

        message = await self.message_service.create_item(
            sender_id=sender.id,
            recipient_id=recipient.id,
            content=message_info.content
        )

        recipient_settings = await self.direct_user_settings_service.get_item_by(
            chat_id=chat.id,
            user_id=recipient.id
        )

        if (recipient_settings.enable_notifications
                and recipient.settings.direct_notifications):

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

        user_settings = await self.direct_user_settings_service.get_item_by(
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

        await self.direct_user_settings_service.update_item(
            user_settings, **settings.dict()
        )

        return user_settings




    async def ban_direct(
            self,
            current_user: User,
            to_ban_user: User
    ):
        chat = await self.get_direct(current_user, to_ban_user)

        if chat.banned_user_id:
            raise EntityBadRequestError(str(chat), "Чат уже заблокирован")

        await self.update_item(chat, banned_user_id=current_user.id)

    async def unban_direct(
            self,
            current_user: User,
            to_unban_user: User
    ):
        chat = await self.get_direct(current_user, to_unban_user)

        if chat.banned_user_id != current_user.id:
            raise EntityBadRequestError(str(chat), "Невозможно разблокировать чат")

        await self.update_item(chat, banned_user_id=None)


    async def get_user_chats(self, user: User, pagination: Pagination) -> list[DirectChatShow]:

        result = await self.repository.get_user_chats(user_id=user.id, **pagination.get())
        return [DirectChatShow(settings=settings, user=user) for settings, user in result]



    async def get_message_by_id(self, user: User, message_id: int) -> DirectMessage:
        message = await self.message_service.get_item_by_id(message_id)

        if user.id not in (message.recipient_id, message.sender_id):
            raise EntityNotFoundError("Сообщение", id=message_id)

        return message

    async def edit_message(self, user: User,  message_id: int, message_updates: MessageCreate) -> DirectMessage:
        message = await self.get_message_by_id(user, message_id)

        if message.sender_id != user.id:
            raise EntityBadRequestError(
                "Сообщение",
                f"{user.username} не владелец сообщения {message_id}"
            )

        message = await self.message_service.update_item(message, **message_updates.dict())

        await self.ws_manager.edit_message(
            recipient_id=message.recipient_id,
            message_id=message_id,
            content=message_updates.content,
            username=user.username
        )
        return message






    async def get_direct(self, user1: User, user2: User) -> DirectChat:
        direct = await self.repository.chat_exists(user1.id, user2.id)

        if direct:
            return direct

        raise EntityNotFoundError(
            "Личный чат",
            username1=user1.username,
            username2=user2.username
        )

    async def get_banned_chats(
            self,
            user: User,
            pagination: Pagination
    ):
        return await self.repository.get_any_by(
            banned_user_id=user.id, **pagination.get()
        )

