from typing import Annotated

from fastapi import Depends

from core.db import getSessionDep
from topic.model import Topic, TopicOffer
from topic.service import TopicOfferService, TopicService


def get_topic_service(
        session: getSessionDep
) -> TopicService:
    return TopicService(session=session)

def get_topic_offer_service(
        session: getSessionDep
) -> TopicOfferService:
    return TopicOfferService(session=session)


topicServiceDep = Annotated[TopicService, Depends(get_topic_service)]
topicOfferServiceDep = Annotated[TopicOfferService, Depends(get_topic_offer_service)]


async def get_topic(
        slug: str,
        topic_service: topicServiceDep,
) -> Topic:
    return await topic_service.get_item_by(slug=slug)

async def get_topic_offer(
        offer_id: int,
        topic_service: topicOfferServiceDep
) -> TopicOffer:
    return await topic_service.get_item_by_id(offer_id)


topicOfferDep = Annotated[TopicOffer, Depends(get_topic_offer)]
topicDep = Annotated[Topic, Depends(get_topic)]



