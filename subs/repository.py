from sqlalchemy.ext.asyncio import AsyncSession

from core.repository import BaseRepository
from subs.model import Subscribe



class SubscribeRepository(BaseRepository[Subscribe]):

    def __init__(self, session: AsyncSession):
        super().__init__(Subscribe, session)







