from httpx import AsyncClient
from pydantic import BaseModel, ValidationError

from integrations.exceptions import ExternalApiRequestError
from integrations.external_api import ExternalAPI, safe_request


class CryptoResponse(BaseModel):
    symbol: str
    price: float


class BinanceAPI(ExternalAPI):

    @safe_request
    async def get_crypto_info(
            self,
            ticker: str = "btc",
    ) -> CryptoResponse:

        async with AsyncClient(base_url=self.path) as client:

            response = await client.get(
                "/ticker/price",
                params={"symbol": f"{ticker.upper()}USDT"}
            )
            data = response.json()

            try:
                data = CryptoResponse.model_validate(data)

            except ValidationError:
                raise ExternalApiRequestError(data)

            return data


binance_client = BinanceAPI("https://api.binance.com/api/v3")