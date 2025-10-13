from core.schemas import BaseSchema, IdMixinSchema, TimeMixinSchema
from post.schemas import PostSlug
from user.schemas import UserUsername


class CommentBase(BaseSchema):
    content: str


class CommentCreate(CommentBase):
    parent_id: int | None = None


class CommentShow(CommentCreate, IdMixinSchema, TimeMixinSchema):
    author: UserUsername
    post: PostSlug


class CommentUpdate(CommentBase):
    ...





