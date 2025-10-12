from fastapi import APIRouter, Depends
from user.deps import userDep
from direct.schemas import  MessageCreate, DirectMessageShow, DirectChatShow, DirectUserSettingsSchema
from auth.deps import currentUserDep
from auth.deps import currentUserDep

from direct.deps import directChatServiceDep
from helpers.search import Pagination

from fastapi_cache.decorator import cache

direct_router = APIRouter(prefix="/direct", tags=["💭 Личные сообщения"])



@direct_router.get(
    "",
    summary="Получить чаты с пользователями",
    response_model=list[DirectChatShow]
)
async def get_user_chats(
        user: currentUserDep,
        direct_service: directChatServiceDep,
        pagination: Pagination = Depends()
):
    return await direct_service.get_user_chats(user, pagination)


@direct_router.get(
    "/banned",
    summary="Получить Заблокированные чаты",
    response_model=list[DirectChatShow]
)
async def get_banned_chats(
        user: currentUserDep,
        chat_service: directChatServiceDep,
        pagination: Pagination = Depends(),
):
    return await chat_service.get_banned_chats(user, pagination)

@direct_router.get(
    "/{username}",
    summary="Получить сообщения чата с пользователем",
    response_model=list[DirectMessageShow]
)
async def get_messages(
        user: currentUserDep,
        recipient: userDep,
        chat_service: directChatServiceDep,
        pagination: Pagination = Depends()
):
    return await chat_service.message_service.get_messages(user, recipient, pagination)


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
    "/{username}/ban",
    summary="Заблокировать Пользователя",
)
async def ban_user(
        current_user: currentUserDep,
        to_ban_user: userDep,
        chat_service: directChatServiceDep,
):
    await chat_service.ban_direct(current_user, to_ban_user)


@direct_router.post(
    "/{username}/unban",
    summary="Разблокировать Пользователя",
)
async def unban_user(
        current_user: currentUserDep,
        to_unban_user: userDep,
        chat_service: directChatServiceDep,
):
    await chat_service.unban_direct(current_user, to_unban_user)





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


@direct_router.get(
    "/msg/{message_id}",
    summary="Получить сообщениe",
    response_model=DirectMessageShow
)
@cache(expire=60)
async def get_message(
        message_id: int,
        user: currentUserDep,
        chat_service: directChatServiceDep,
):
    return await chat_service.get_message_by_id(user, message_id)


@direct_router.put(
    "/msg/{message_id}",
    summary="Изменить сообщениe",
    response_model=DirectMessageShow
)
async def edit_message(
        message_id: int,
        user: currentUserDep,
        chat_service: directChatServiceDep,
        updates: MessageCreate
):
    return await chat_service.edit_message(user, message_id, updates)






