from fastapi import APIRouter
from fastapi_cache.decorator import cache

from integrations.university.external import UniversityAPI,Group,  ErrorResponse,TimeTableResponse, university_client

university_router = APIRouter(prefix="/ext/university", tags=["🗒 Расписание"])


@university_router.get(
    "/groups",
    summary="Получить группы"
)
async def get_groups(
        count: int,
) -> list[Group]:
    return await university_client.get_groups(count)



@university_router.get(
    "/tt/{group}",
    summary="Получить расписание группы"
)
async def get_timetable(
        group: str,
) -> TimeTableResponse | ErrorResponse:
    return await university_client.get_timetable(group)




