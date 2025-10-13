from functools import partial

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import EntityBadRequestError
from core.service import BaseService
from direct.ws import WebSocketManager
from helpers.search import Pagination
from post.model import Post
from post.schemas import PostReactions
from reaction.model import Reaction
from reaction.repository import ReactionRepository
from user.model import User

from reaction.types import PostReactionsSetParams

class ReactionService(BaseService[Reaction, ReactionRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(Reaction, session, ReactionRepository)
        self.ws_manager = WebSocketManager()

    async def add_reaction(self, user: User, post: Post, reaction_type: PostReactionsSetParams):
        if not post.allow_reactions:
            raise EntityBadRequestError(
                "Reaction",
                f"Под постом [{post.slug}] запрещено оставлять реакции"
            )

        reaction = await self.repository.get_one_by(user_id=user.id, post_id=post.id)

        if reaction:
            await self.delete_item(reaction)

        reaction = await self.create_item(user_id=user.id, post_id=post.id, reaction=reaction_type)

        if reaction.user.settings.reaction_notifications:
            await self.ws_manager.reaction_notify(
                recipient_id=post.author_id,
                reaction=reaction_type,
                username=user.username,
                post_id=post.id
            )

        return reaction


    async def get_post_reactions(self, post: Post, reaction_type: str, pagination: Pagination) -> list[Reaction]:
        default_get = partial(self.repository.get_any_by, post_id=post.id, **pagination.dict())

        return await self._get_reactions(default_get, reaction_type)


    async def get_user_reactions(self, user: User, reaction_type: str, pagination: Pagination) -> list[Reaction]:
        default_get = partial(self.repository.get_any_by, user_id=user.id, **pagination.dict())

        return await self._get_reactions(default_get, reaction_type)


    async def get_post_reaction_count(self, post: Post) -> PostReactions:
        reactions = await self.repository.get_post_reaction_count(post=post)

        return PostReactions(**reactions)

    async def _get_reactions(self, default, reaction):
        if reaction == "all":
            return await default()
        return await default(reaction=reaction)








