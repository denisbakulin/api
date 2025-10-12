from fastapi import APIRouter, Depends, status
from auth.deps import currentUserDep, adminDep, get_admin


from topic.deps import topicOfferServiceDep, topicDep, topicServiceDep, topicOfferDep
from topic.schemas import BaseTopic, TopicOfferShow, AddTopicByOffer, CreateTopic
from fastapi import status
from post.deps import postServiceDep
from post.schemas import PostShow, PostCreate
from helpers.search import Pagination

topic_router = APIRouter(prefix="/topics", tags=["📚 Темы"])


@topic_router.get(
    "",
    summary="Получить темы",
    response_model=list[BaseTopic]
)
async def get_topics(
        topic_service: topicServiceDep,
        pagination: Pagination = Depends()
):
    return await topic_service.get_items_by(pagination)



@topic_router.post(
    "",
    summary="Создать тему",
    response_model=BaseTopic,
    dependencies=[Depends(get_admin)],
    status_code=status.HTTP_201_CREATED
)
async def create_topic(
        topic_service: topicServiceDep,
        topic: CreateTopic,
):
    return await topic_service.create_topic(topic)



@topic_router.post(
    "/offer",
    summary="Предложить тему для обсуждений",
    response_model=TopicOfferShow,
    status_code=status.HTTP_201_CREATED,
)
async def offer_theme(
        user: currentUserDep,
        offer_service: topicOfferServiceDep,
        topic: BaseTopic
):
    return await offer_service.create_offer_topic(user, topic)


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
    response_model=BaseTopic
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
        post_info: PostCreate,
        user: currentUserDep,
        post_service: postServiceDep,

):
    return await post_service.create_post(user, post_info, topic_id=topic.id)


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
    return await post_service.get_items_by(pagination, topic_id=topic.id)





@topic_router.post(
    "/offer/{offer_id}/process",
    summary="Принять/отклонить тему",
    response_model=BaseTopic,
    dependencies=[Depends(get_admin)],
    status_code=status.HTTP_201_CREATED
)
async def process_topic(
        topic_offer: topicOfferDep,
        topic_service: topicServiceDep,
        process: AddTopicByOffer,
):
    return await topic_service.create_topic_from_offer(
        process=process, topic=topic_offer
    )








