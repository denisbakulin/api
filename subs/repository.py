from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.repository import BaseRepository
from subs.model import Subscribe
from user.model import User


class SubscribeRepository(BaseRepository[Subscribe]):

    def __init__(self, session: AsyncSession):
        super().__init__(Subscribe, session)







