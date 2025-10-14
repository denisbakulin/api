from core.schemas import BaseSchema, TimeMixinSchema
from user.schemas import UserShow

class SubscribeShow(BaseSchema, TimeMixinSchema):
    creator: UserShow