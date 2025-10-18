from fastapi import APIRouter
from fastapi_cache.decorator import cache

from integrations.crypto.external import CryptoResponse, binance_client

crypto_router = APIRouter(prefix="/ext/crypto", tags=["💰 Криптовалюты"])


@crypto_router.get(
    "/{ticker}",
    summary="Получить курс криптоволюты в USDT"
)
@cache(expire=60)
async def get_crypto(
        ticker: str,
) -> CryptoResponse:

    return await binance_client.get_crypto_info(ticker)



