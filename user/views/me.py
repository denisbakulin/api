from fastapi import APIRouter, Depends

from auth.deps import currentUserDep
from comment.deps import commentServiceDep
from comment.schemas import CommentShow
from helpers.search import Pagination

from reaction.deps import reactionServiceDep
from reaction.schemas import ReactionShow
from reaction.types import UserReactions
from user.deps import userServiceDep
from user.schemas import PasswordChange, PasswordCreate, UserShowMe, UserUpdate, UserSettings


me_router = APIRouter(prefix="/me", tags=["👤 Личный кабинет"])


@me_router.get(
    "",
    summary="Получить текущего пользователя",
    response_model=UserShowMe,
)
async def get_me(
        user: currentUserDep
):
    return user


@me_router.patch(
    "",
    summary="Изменить информацию текущего пользователя"
)
async def patch_my_info(
        user_updates: UserUpdate,
        user: currentUserDep,
        user_service: userServiceDep,
):
    await user_service.update_user(user, user_updates)




@me_router.put(
    "/password",
    summary="Изменить пароль"
)
async def change_password(
        pwd: PasswordChange,
        user: currentUserDep,
        user_service: userServiceDep,
):
    await user_service.change_password(user, pwd.old_password, pwd.new_password)



@me_router.post(
    "/password",
    summary="Создать пароль"
)
async def set_password(
        pwd: PasswordCreate,
        user: currentUserDep,
        user_service: userServiceDep,
):
    await user_service.set_password(user, pwd)


@me_router.get(
    "/settings",
    summary="Получить настройки аккаунта",
    response_model=UserSettings
)
async def get_settings(
        user: currentUserDep,
):

    return user.settings


@me_router.patch(
    "/settings",
    summary="Изменить настройки аккаунта",
    response_model=UserSettings
)
async def edit_settings(
        user: currentUserDep,
        user_service: userServiceDep,
        settings: UserSettings
):
    return await user_service.edit_user_settings(user, settings)


@me_router.get(
    "/comments",
    summary="Получить комментарии текущего пользователя",
    response_model=list[CommentShow],

)
async def get_my_comments(
        user: currentUserDep,
        comment_service: commentServiceDep,
        pagination: Pagination = Depends()

):
    return await comment_service.get_user_comments(user=user, pagination=pagination)


@me_router.get(
    "/reactions",
    summary="Получить реакции пользователя",
    response_model=list[ReactionShow],

)
async def get_my_reactions(
        user: currentUserDep,
        like_service: reactionServiceDep,
        v: UserReactions,
        pagination: Pagination = Depends()
):
    return await like_service.get_user_reactions(user, v, pagination)


from fastapi import status

from post.deps import postServiceDep
from post.schemas import PostShow, UserPostCreate


@me_router.post(
    "/posts",
    summary="Создать пост",
    response_model=list[PostShow],
    status_code=status.HTTP_201_CREATED,

)
async def create_post(
        post_info: UserPostCreate,
        user: currentUserDep,
        post_service: postServiceDep,
):
    return await post_service.create_post(user, post_info)











