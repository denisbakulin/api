
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import EntityBadRequestError
from core.service import BaseService
from direct.ws import WebSocketManager
from helpers.search import Pagination
from post.model import Post

from reaction.model import Reaction
from reaction.repository import ReactionRepository
from user.model import User
from topic.model import Topic
from reaction.types import ReactionsSetParams
from functools import partial
from reaction.schemas import ReactionsCount
class ReactionService(BaseService[Reaction, ReactionRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(Reaction, session, ReactionRepository)
        self.ws_manager = WebSocketManager()

    async def add_reaction(
            self,
            user: User,
            reaction_type: ReactionsSetParams,
            post: Post | None = None,
            topic: Topic | None = None
    ):
        partial_get = partial(self.repository.get_one_by, user_id=user.id)
        partial_set = partial(self.create_item, user_id=user.id, reaction=reaction_type)

        if post:
            if not post.allow_reactions:
                raise EntityBadRequestError(
                    "Reaction",
                    f"Под постом [{post.slug}] запрещено оставлять реакции"
                )
            reaction = await partial_get(post_id=post.id)
        else:
            reaction = await partial_get(topic_id=topic.id)

        if reaction:
            await self.delete_item(reaction)

        if post:
            return await partial_set(post_id=post.id)
        return await partial_set(topic_id=topic.id)



    async def get_post_reactions(self, post: Post, reaction_type: str, pagination: Pagination) -> list[Reaction]:
        default_get = partial(self.repository.get_any_by, post_id=post.id, **pagination.dict())

        return await self._get_reactions(default_get, reaction_type)

    async def get_topic_reactions(self, topic: Topic, reaction_type: str, pagination: Pagination) -> list[Reaction]:
        default_get = partial(self.repository.get_any_by, topic_id=topic.id, **pagination.dict())

        return await self._get_reactions(default_get, reaction_type)


    async def get_user_reactions(self, user: User, reaction_type: str, pagination: Pagination) -> list[Reaction]:
        default_get = partial(self.repository.get_any_by, user_id=user.id, **pagination.dict())

        return await self._get_reactions(default_get, reaction_type)


    async def get_post_reaction_count(self, post: Post) -> ReactionsCount:
        reactions = await self.repository.get_post_reaction_count(post=post)

        return ReactionsCount(**reactions)

    async def _get_reactions(self, default, reaction):
        if reaction == "all":
            return await default()
        return await default(reaction=reaction)








