from pydantic import BaseModel

from core.schemas import TimeMixinSchema


class ReactionShow(BaseModel, TimeMixinSchema):
    user_id: int
    post_id: int
    reaction: str

