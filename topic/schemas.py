from core.schemas import BaseSchema, IdMixinSchema
from topic.model import TopicOfferStatus
from user.schemas import UserUsername


class CreateTopicOffer(BaseSchema):
    title: str
    description: str


class CreateTopic(CreateTopicOffer):
    slug: str


class TopicOfferShow(CreateTopicOffer, IdMixinSchema):
    status: TopicOfferStatus
    author: UserUsername
    process_user: UserUsername | None


class TopicShow(CreateTopic):
    approved_user: UserUsername
    suggested_by_user: UserUsername | None


class AddTopicByOffer(CreateTopic):
    status: TopicOfferStatus


class UserCommentsCountOfTopicShow(BaseSchema):
    count: int
    topic: TopicShow

