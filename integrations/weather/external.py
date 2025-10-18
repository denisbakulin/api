from httpx import AsyncClient
from pydantic import BaseModel, ValidationError

from integrations.exceptions import ExternalApiRequestError
from integrations.external_api import ExternalAPI, safe_request


class WeatherResponse(BaseModel):
    city: str
    temp: float
    feel_like: float
    weather: str
    humidity: float
    wind_speed: float


class OpenWeatherAPI(ExternalAPI):

    @safe_request
    async def get_city_weather(self, city: str):

        async with AsyncClient(base_url=self.path) as client:
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric",
                "lang": "ru",
            }
            response = await client.get("/data/2.5/weather", params=params)
            data = response.json()

            try:
                res = WeatherResponse.model_validate(dict(
                    city=data["name"],
                    temp=data["main"]["temp"],
                    feel_like=data["main"]["feels_like"],
                    weather=data["weather"][0]["description"],
                    humidity=data["main"]["humidity"],
                    wind_speed=data["wind"]["speed"],
                ))
            except (ValidationError, KeyError):
                raise ExternalApiRequestError(data)

        return res



openweather_client = OpenWeatherAPI(
    "https://api.openweathermap.org",
    "565b6c3459edaffcef3b889efa0903c4"
)

