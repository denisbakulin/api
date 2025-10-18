"""
timetable/get?groupName=%22%D0%91%D0%9F%D0%9825-02%22"""

from httpx import AsyncClient
from pydantic import BaseModel, ValidationError, field_serializer

from integrations.exceptions import ExternalApiRequestError
from integrations.external_api import ExternalAPI, safe_request
from datetime import datetime
from datetime import time
import re

class SubLesson(BaseModel):
    name: str
    type: str
    teacher: str
    place: str

    @field_serializer("place")
    def serialize_period(self, place: str):
        place = re.sub(r'["\\]+', '', place).split()
        return place[1] + place[-1]






class LessonTime(BaseModel):
    start: time
    end: time

class Lesson(BaseModel):
    period: str
    sub_lessons: list[SubLesson]

    @field_serializer("period")
    def serialize_period(self, period: str):
        start, end = period.split()[0].split("-")
        return LessonTime(start=start, end=end)


class Day(BaseModel):
    name: str
    today: bool = False
    lessons: list[Lesson]

    @field_serializer("today")
    def serialize_today(self, today):
        return "сегодня" in self.name
    @field_serializer("name")
    def serialize_name(self, name: str):
        if "сегодня" in name:
            return name.split()[0]
        return name




class Week(BaseModel):
    name: str
    days: list[Day]



class TimeTableResponse(BaseModel):
    name: str
    semester: int
    date: str
    week: list[Week]

    @field_serializer("name")
    def serialize_name(self, name: str):
        name = re.sub(r'["\\]+', '', name)
        return name


class Group(BaseModel):
    ID: int
    Name: str
    PalladaKey: int

class ErrorResponse(BaseModel):
    message: str

class UniversityAPI(ExternalAPI):

    @safe_request
    async def get_timetable(self, group: str) -> TimeTableResponse | ErrorResponse:

       async with AsyncClient(base_url=self.path) as client:
           response = await client.get(
               "/timetable/get",
               params={"groupName": f'"{group}"'}
           )
           print(response.url, response.json())
           if response.status_code == 400:
               return ErrorResponse(message="руппа не найдена")

           return TimeTableResponse.model_validate(response.json())


    @safe_request
    async def get_groups(self, count: int) -> list[Group]:
        async with AsyncClient(base_url=self.path) as client:
           response = await client.get(
               "/groups/get",
               params={"count": count}
           )
           print(response.json(), response.url)

           return [Group.model_validate(model) for model in response.json()]




"""https://tt.sibgu.moxitech.ru/api/groups/get?count=100"""
"""https://tt.sibgu.moxitech.ru/api/feeds/get"""
"""https://tt.sibgu.moxitech.ru/api/timetable/professor/get?professorName"""
"""https://tt.sibgu.moxitech.ru/api/professors/get?count=1000"""


university_client = UniversityAPI("https://tt.sibgu.moxitech.ru/api")