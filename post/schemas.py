from pydantic import BaseModel, Field

from core.schemas import BaseSchema, IdMixinSchema, TimeMixinSchema
from topic.schemas import TopicSlug
from reaction.schemas import ReactionsCount

class PostAllows(BaseSchema):
    allow_comments: bool = Field(default=True)
    allow_reactions: bool = Field(default=True)
    public: bool = Field(default=True)


class PostBase(BaseSchema):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(max_length=5000)

from user.schemas import UserUsername


class PostShow(PostBase, IdMixinSchema, TimeMixinSchema):
    author: UserUsername
    slug: str
    topic: TopicSlug | None


class PostSlug(BaseSchema):
    slug: str

class TopPostShow(BaseSchema):
    post: PostShow
    count: int


class FullPostShow(BaseSchema):
    post: PostShow
    reactions: ReactionsCount



class PostCreate(PostBase):
    ...

class UserPostCreate(PostCreate, PostAllows):
    ...


class PostUpdate(BaseSchema):
    content: str = Field(max_length=5000)
    public: bool




