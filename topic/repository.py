from sqlalchemy.ext.asyncio import AsyncSession

from core.repository import BaseRepository
from topic.model import Topic, TopicOffer
from sqlalchemy import select, func, distinct
from post.model import Post
from comment.model import Comment
from typing import TypeAlias


full_topic: TypeAlias = tuple[Topic, int, int]

class TopicRepository(BaseRepository[Topic]):

    def __init__(self, session: AsyncSession):
        super().__init__(Topic, session)


    async def get_topics_with_content_counts(
            self, offset: int | None = None,
            limit: int | None = None,
            topic_id: int | None = None
    ) -> list[full_topic] | full_topic:
        """Возвращает topic и количество постов, комментариев под ним """

        stmt = (
            select(Topic, func.count(distinct(Post.id)), func.count(Comment.id))
            .select_from(Topic)
            .outerjoin(
                Post, Topic.id == Post.topic_id
            )
            .outerjoin(
                Comment, Comment.post_id == Post.id
            )
            .group_by(Topic.id)
        )

        if topic_id:
            stmt = stmt.where(Topic.id == topic_id)
        else:
            stmt = stmt.offset(offset).limit(limit)

        res = await self.session.execute(stmt)

        if topic_id:
            return res.tuples().first()
        return [*res.tuples().all()]

class TopicOfferRepository(BaseRepository[TopicOffer]):

    def __init__(self, session: AsyncSession):
        super().__init__(TopicOffer, session)







