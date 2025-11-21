from fastapi import APIRouter, Depends

from user.deps import userDep, userServiceDep
from user.schemas import UserShow, UserCreate
from user.utils import UserSearchParams

from auth.deps import admin_validate, get_current_user

user_router = APIRouter(prefix="/users", tags=["👨 Пользователи"])

@user_router.get(
    "/search",
    summary="Поиск пользователя по ключевым параметрам",
    response_model=list[UserShow],
)
async def search_users(
        user_service: userServiceDep,
        search: UserSearchParams = Depends(),
):
    return await user_service.search_users(search=search)


@user_router.get(
    "/@{username}",
    summary="Получить пользователя по username",
    response_model=UserShow,
)
async def get_user(
        user: userDep
):
    return user


@user_router.post(
    "",
    summary="Создать пользователя",
    response_model=UserShow,
    dependencies=[Depends(admin_validate)]
)
async def create_user(
        create: UserCreate,
        service: userServiceDep
):
    return await service.create_user(create)


@user_router.get(
    "/me",
    summary="me",
    response_model=UserShow,
)
async def me(
        user= Depends(get_current_user)
):
    return user


@user_router.get(
    "",
    summary="all",
    response_model=list[UserShow],
    dependencies=[Depends(admin_validate)]
)
async def me(
    service: userServiceDep
):
    return await service.get_items_by()



