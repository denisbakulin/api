from sqlalchemy.ext.asyncio import AsyncSession

from comment.model import Comment
from comment.repository import CommentRepository
from comment.schemas import CommentCreate, CommentUpdate
from core.exceptions import EntityBadRequestError
from core.service import BaseService
from direct.manager import WebSocketManager
from helpers.search import Pagination
from post.model import Post
from post.service import PostService
from topic.schemas import UserCommentsCountOfTopicShow
from user.model import User
from user.service import UserService


class CommentService(BaseService[Comment, CommentRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(Comment, session, CommentRepository)
        self.user_service = UserService(session=session)
        self.post_service = PostService(session=session)
        self.ws_manager = WebSocketManager()


    async def create_comment(
            self,
            comment_data: CommentCreate,
            user: User,
            post: Post
    ) -> Comment:
        if not post.allow_comments:
            raise EntityBadRequestError(
                "Comment",
                f"Под постом [{post.slug}] нельзя оставлять комментарии"
            )

        if comment_data.parent_id is not None:
            parent = await self.get_comment_by_id(comment_data.parent_id)
            if parent.post_id != post.id:
                raise EntityBadRequestError(
                    "Comment",
                    "Родителький комментарий не принадлежит указанному посту"
                )

        comment = await self.create_item(
            **comment_data.model_dump(exclude_none=True),
            user_id=user.id, post_id=post.id,
        )

        if post.author.settings.comment_notifications:
            await self.ws_manager.comment_notify(
                recipient_id=post.author_id,
                username=user.username,
                comment=comment.content[:100],
                comment_id=comment.id
            )

        return comment

    async def update_comment(
            self,
            comment: Comment,
            user: User,
            update_data: CommentUpdate
    ) -> Comment:

        if comment.user_id != user.id:
            raise EntityBadRequestError(
                "Comment",
                f"Комментарий id={comment.id} не принадлежит user={user.username}"
            )

        await self.update_item(comment, **update_data.model_dump())

        return comment

    async def get_comment_by_id(self, comment_id: int) -> Comment:
        return await self.get_item_by_id(comment_id)

    async def get_post_comments(self, post: Post, pagination: Pagination) -> list[Comment]:
        return await self.repository.get_any_by(post_id=post.id, **pagination.get())

    async def get_user_comments(self, user: User, pagination: Pagination) -> list[Comment]:
        return await self.repository.get_any_by(user_id=user.id, **pagination.get())


    async def get_top_themes_of_user(
            self,
            user: User
    ) -> list[UserCommentsCountOfTopicShow]:
        top_themes = await self.repository.get_user_comment_count_by_topic(
            user.id
        )
        return [
            UserCommentsCountOfTopicShow(topic=topic, count=count)
            for topic, count in top_themes
        ]














