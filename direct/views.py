from fastapi import APIRouter, Depends

from auth.deps import currentUserDep
from direct.deps import directChatServiceDep
from direct.schemas import (DirectChatShow, DirectMessageShow,
                            DirectUserSettingsSchema, MessageCreate)

from user.deps import userDep

direct_router = APIRouter(prefix="/direct", tags=["💭 Личные сообщения"])



@direct_router.get(
    "",
    summary="Получить чаты с пользователями",
    response_model=list[DirectChatShow]
)
async def get_user_chats(
        user: currentUserDep,
        direct_service: directChatServiceDep,
):
    return await direct_service.get_user_chats(user)



@direct_router.get(
    "/{username}",
    summary="Получить сообщения чата с пользователем",
    response_model=list[DirectMessageShow]
)
async def get_messages(
        user: currentUserDep,
        recipient: userDep,
        chat_service: directChatServiceDep,
):
    return await chat_service.message_service.get_messages(user, recipient)


@direct_router.get(
    "/{username}/settings",
    summary="Получить настройки чата",
    response_model=DirectUserSettingsSchema
)
async def get_direct_settings(
        user: currentUserDep,
        recipient: userDep,
        chat_service: directChatServiceDep,
):
    return await chat_service.get_direct_settings(user, recipient)


@direct_router.patch(
    "/{username}/settings",
    summary="Изменить настройки чата",
    response_model=DirectUserSettingsSchema
)
async def edit_direct_settings(
        user: currentUserDep,
        recipient: userDep,
        settings: DirectUserSettingsSchema,
        chat_service: directChatServiceDep,
):
    return await chat_service.edit_direct_settings(user, recipient, settings)



@direct_router.post(
    "/msg/{username}",
    summary="Отправить сообщение пользователю",
    response_model=DirectMessageShow
)
async def create_message(
        sender: currentUserDep,
        recipient: userDep,
        chat_service: directChatServiceDep,
        message_info: MessageCreate

):
    return await chat_service.create_message(sender, recipient, message_info)








