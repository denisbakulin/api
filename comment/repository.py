from typing import Optional

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from comment.model import Comment
from core.repository import BaseRepository
from post.model import Post
from topic.model import Topic


class CommentRepository(BaseRepository[Comment]):

    def __init__(self, session: AsyncSession):
        super().__init__(Comment, session)

    async def create_comment(
            self,
            **comment_data,
    ) -> Comment:
        return self.create(**comment_data)

    async def get_comments(
            self,
            offset: Optional[int],
            limit: Optional[int],
            **filters,
    ) -> list[Comment] | None:
        return await self.get_any_by(offset=offset, limit=limit, **filters)

    async def get_comment(
            self,
            **filters
    ) -> Optional[Comment]:
        return await self.get_one_by(**filters)


    async def get_user_comment_count_by_topic(
            self,
            user_id: int,
    ) -> list[tuple[Topic, int]]:
        stmt = (
            select(
                Topic,
                func.count(Comment.id)
            )
            .join(
                Post, Post.topic_id == Topic.id
            )
            .join(
                Comment, Comment.post_id == Post.id
            )
            .where(Comment.user_id == user_id)
            .group_by(Topic.id)
            .limit(10)
        )

        result = await self.session.execute(stmt)


        return [*result.tuples().all()]





