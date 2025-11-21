from sqlalchemy.ext.asyncio import AsyncSession

from core.repository import BaseRepository
from user.model import User


class UserRepository(BaseRepository[User]):

    def __init__(self, session: AsyncSession):
        super().__init__(User, session)




