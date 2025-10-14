from pydantic import BaseModel

from core.schemas import TimeMixinSchema, BaseSchema
from user.schemas import UserUsername

class ReactionsCount(BaseModel):
    like: int = 0
    love: int = 0
    dislike: int = 0


class Slug(BaseSchema):
    slug: str


class BaseReactionShow(BaseSchema, TimeMixinSchema):
    reaction: str
    user: UserUsername

class PostReactionShow(BaseReactionShow, TimeMixinSchema):
    post: Slug

class TopicReactionShow(BaseReactionShow, TimeMixinSchema):
    topic: Slug


