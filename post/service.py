from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import EntityBadRequestError
from core.service import BaseService
from post.model import Post
from post.repository import PostRepository
from post.schemas import PostCreate, PostUpdate, TopPostShow
from post.utils import generate_slug
from user.model import User
from helpers.search import Pagination

class PostService(BaseService[Post, PostRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(Post, session, PostRepository)

    async def create_post(self, user: User, post_create: PostCreate, topic_id: int | None = None) -> Post:

        post = await self.create_item(**post_create.model_dump(), author_id=user.id, topic_id=topic_id)

        slug = generate_slug(post.title, post.id)

        await self.update_item(post, slug=slug)

        return post

    async def get_top_of_posts(self, q: str):

        posts = await self.repository.get_top_of_posts(q)
        return [TopPostShow(post=post, count=count) for post, count in posts]


    async def update_post(self, post: Post, post_update: PostUpdate, user: User) -> Post:

        if post.author_id != user.id:
            raise EntityBadRequestError(
                "Post",
                f"Пост id={post.id} не принадлежит user={user.username}"
            )

        await self.update_item(post, **post_update.model_dump())

        return post

    async def get_user_posts(self, user: User, pagination: Pagination) -> list[Post]:
        return await self.get_items_by(
            user_id=user.id,
            topic_id=None,
            **pagination.dict()
        )

