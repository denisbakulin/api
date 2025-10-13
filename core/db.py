from functools import lru_cache

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from core.model import BaseORM
from core.settings import app_settings
from typing import Annotated
from fastapi import Depends


@lru_cache
def get_engine():
    return create_async_engine(app_settings.db_uri, echo=True)

session_factory = async_sessionmaker(bind=get_engine(), expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with session_factory() as session:
        yield session


async def init_models():
    async with get_engine().begin() as conn:
        await conn.run_sync(BaseORM.metadata.create_all)



getSessionDep = Annotated[AsyncSession, Depends(get_session)]
