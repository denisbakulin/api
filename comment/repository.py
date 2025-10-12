from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, and_
from comment.model import Comment
from core.repository import BaseRepository
from sqlalchemy import select
from topic.model import Topic
from post.model import Post

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

        q = result.tuples().all()

        print(q, 1111111111111111111111111111111111111111111)

        return [*q]





