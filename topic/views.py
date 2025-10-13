from fastapi import APIRouter, Depends, status

from auth.deps import currentUserDep, role_validate
from helpers.search import Pagination
from post.deps import postServiceDep
from post.schemas import PostCreate, PostShow
from topic.deps import (topicDep, topicOfferDep, topicOfferServiceDep,
                        topicServiceDep)
from topic.schemas import (AddTopicByOffer, CreateTopicOffer, TopicOfferShow,
                           TopicShow, CreateTopic)
from user.model import UserRoleEnum, User

topic_router = APIRouter(prefix="/topics", tags=["📚 Темы"])


@topic_router.get(
    "",
    summary="Получить темы",
    response_model=list[TopicShow]
)
async def get_topics(
        topic_service: topicServiceDep,
        pagination: Pagination = Depends()
):
    return await topic_service.get_items_by(pagination)



@topic_router.post(
    "",
    summary="Создать тему",
    response_model=TopicShow,
    status_code=status.HTTP_201_CREATED
)
async def create_topic(
        topic: CreateTopic,
        topic_service: topicServiceDep,
        user: User = Depends(role_validate(UserRoleEnum.MODERATOR, ))
):
    return await topic_service.create_topic(
        topic=topic, approved_user=user, suggested_user=user
    )



@topic_router.post(
    "/offer",
    summary="Предложить тему для обсуждений",
    response_model=TopicOfferShow,
    status_code=status.HTTP_201_CREATED,
)
async def offer_theme(
        topic_create: CreateTopicOffer,
        user: currentUserDep,
        offer_service: topicOfferServiceDep,

):
    return await offer_service.create_offer_topic(
        author=user, topic_create=topic_create
    )


@topic_router.get(
    "/offer",
    summary="Посмотреть предложенные темы",
    response_model=list[TopicOfferShow],
)
async def offer_theme(
        offer_service: topicOfferServiceDep,
        pagination: Pagination = Depends()
):
    return await offer_service.get_items_by(pagination)


@topic_router.get(
    "/{slug}",
    summary="Получить тему",
    response_model=TopicShow
)
async def get_topic(
        topic: topicDep
):
    return topic

@topic_router.post(
    "/{slug}/posts",
    summary="Создать пост",
    response_model=PostShow,
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
        topic: topicDep,
        post_create: PostCreate,
        user: currentUserDep,
        post_service: postServiceDep,

):
    return await post_service.create_post(
        user=user, post_create=post_create, topic_id=topic.id
    )


@topic_router.get(
    "/{slug}/posts",
    summary="Получить посты по теме",
    response_model=list[PostShow]
)
async def get_topic_posts(
        topic: topicDep,
        post_service: postServiceDep,
        pagination: Pagination = Depends()
):
    return await post_service.get_items_by(
        topic_id=topic.id, pagination=pagination
    )





@topic_router.post(
    "/offer/{offer_id}/process",
    summary="Принять/отклонить тему",
    response_model=TopicOfferShow | TopicShow,
    status_code=status.HTTP_201_CREATED
)
async def process_topic(
        topic_offer: topicOfferDep,
        topic_service: topicServiceDep,
        process: AddTopicByOffer,
        user = Depends(role_validate(UserRoleEnum.MODERATOR, ))
):
    return await topic_service.create_topic_from_offer(
        process=process, topic=topic_offer, process_user=user
    )








