from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.repository import BaseRepository
from post.model import Post
from reaction.model import Reaction


class ReactionRepository(BaseRepository[Reaction]):

    def __init__(self, session: AsyncSession):
        super().__init__(Reaction, session)

    async def get_post_reaction_count(self, post: Post) -> dict[str, int]:
        stmt = (
            select(
                Reaction.reaction,
                func.count().label("count")
            )
            .where(Reaction.post_id == post.id)
            .group_by(Reaction.reaction)
        )

        result = await self.session.execute(stmt)

        return {reaction: count for reaction, count in result.all()}


