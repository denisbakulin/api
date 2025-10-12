from typing import Optional

from core.schemas import BaseSchema, IdMixinSchema, TimeMixinSchema
from pydantic import Field

class CommentBase(BaseSchema):
    content: str

class CommentCreate(CommentBase):
    parent_id: Optional[int] = Field(default=None)


class CommentShow(CommentCreate, IdMixinSchema, TimeMixinSchema):
    user_id: int
    post_id: int


class CommentUpdate(CommentBase):
    ...





