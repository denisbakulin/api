from typing import Annotated

from fastapi import Depends

from core.db import getSessionDep
from direct.service import DirectChatService


def get_direct_chat_service(
        session: getSessionDep
) -> DirectChatService:
    return DirectChatService(session=session)


directChatServiceDep = Annotated[DirectChatService, Depends(get_direct_chat_service)]




