from pydantic import BaseModel

from core.schemas import BaseSchema, IdMixinSchema, TimeMixinSchema


class MessageCreate(BaseModel):
    content: str


class DirectMessageShow(MessageCreate, TimeMixinSchema, IdMixinSchema):
    recipient_id: int
    sender_id: int

from user.schemas import UserShow


class BaseDirectEvent(BaseModel):
    type: str
    data: dict

class ClientDirectEvent(BaseDirectEvent):
    initiator_id: int



class DirectUserSettingsSchema(BaseSchema):
    chat_name: str | None = None
    enable_notifications: bool | None = None


class DirectChatShow(BaseModel):
    settings: DirectUserSettingsSchema
    user: UserShow

