from typing import Literal

from fastapi import APIRouter, Path
from fastapi_cache.decorator import cache

from integrations.weather.external import (WeatherResponse,
                                           openweather_client)

weather_router = APIRouter(prefix="/ext/weather", tags=["🌤 Погода"])


@weather_router.get(
    "/{city}",
    summary="Получить погоду в городе"
)
@cache(expire=3600)
async def get_weather(
        city: str = Path(description="Название города"),
) -> WeatherResponse:
    return await openweather_client.get_city_weather(city)



