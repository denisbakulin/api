from typing import Any, Optional

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.repository import BaseRepository
from post.model import Post
from reaction.model import Reaction
from subs.repository import SubscribeRepository


class PostRepository(BaseRepository[Post]):

    def __init__(self, session: AsyncSession):
        super().__init__(Post, session)
        self.subs_repository = SubscribeRepository(session)

    async def get_posts(
            self,
            offset: Optional[int],
            limit: Optional[int],
            **filters,
    ) -> list[Post] | None:

        return await self.get_any_by(offset=offset, limit=limit, **filters)

    async def search_posts(
            self,
            offset: int,
            limit: int,
            field: str,
            query: Any,
    ) -> list[Post]:
        return await self.search(field, query, offset=offset, limit=limit)


    async def get_posts_by_user_subscribes(self, user_id: int, offset: int, limit: int) -> list[Post]:
        subs = await self.subs_repository.get_any_by(
            subscriber_id=user_id,  offset=offset, limit=limit
        )

        subs_ids = [sub.creator_id for sub in subs]

        if not subs_ids:
            return []

        stmt = select(Post).where(Post.author_id.in_(subs_ids))

        result = await self.session.execute(stmt)

        posts = result.scalars().all()

        return [*posts]

    async def get_top_of_posts(self, reaction: str):
        stmt = (
            select(
                Post,
                func.count(Reaction.post_id).label("like_count")
            )
            .join(Reaction, Reaction.post_id == Post.id)
            .where(Reaction.reaction == reaction)
            .group_by(Post.id)
            .order_by(desc("like_count"))
            .limit(10)
        )
        result = await self.session.execute(stmt)

        posts = result.all()

        return [*posts]






