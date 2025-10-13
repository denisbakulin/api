from functools import wraps
from typing import Callable, Optional, Self

from fastapi import WebSocket

from direct.schemas import ClientDirectEvent


class WebSocketManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            instance = cls._instance = super().__new__(cls)
            print("WebSocketManager created")
            cls.init(instance)

        return cls._instance


    def init(self):
        print("WebSocketManager init")
        self.connections: dict[int, WebSocket] = {}


    @staticmethod
    def recipient_connected(func):
        """Декоратор, проверяющий существование WebSocket по recipient_id"""

        @wraps(func)
        async def wrapper(*args, recipient_id: int, **kwargs):
            manager = WebSocketManager()
            connection = manager.get_connection(recipient_id)
            print(connection, args, kwargs)

            if connection:
                return func(*args, connection=connection, **kwargs)

        return wrapper


    def connect(self, user_id: int, ws: WebSocket):
        connect = self.connections.get(user_id)
        if connect:
            connect.close()

        self.connections[user_id] = ws

    def get_connection(self, user_id: int) -> Optional[WebSocket]:
        return self.connections.get(user_id)


    @recipient_connected
    async def message_notify(self, connection: WebSocket, *, username: str, message_id: int, message: str):
        await connection.send_json({
            "action": "notify",
            "data": {
                "message_id": message_id,
                "username": username,
                "message": message
            }
        })

    @recipient_connected
    async def reaction_notify(self, connection: WebSocket, *, username: str, reaction: str, post_id: int):
        await connection.send_json({
            "action": "reaction",
            "data": {
                "username": username,
                "reaction": reaction,
                "post_id": post_id
            }
        })

    @recipient_connected
    async def comment_notify(self, connection: WebSocket, *, username: str, comment: str, comment_id: int):
        await connection.send_json({
            "action": "reaction",
            "data": {
                "username": username,
                "comment": comment
            }
        })

    @recipient_connected
    async def edit_message(self, connection: WebSocket, *, username: str, message_id: int, content: str):
        await connection.send_json({
            "action": "edit_message",
            "data": {
                "username": username,
                "message_id": message_id,
                "content": content
            }
        })

    @recipient_connected
    async def user_typing(self, connection: WebSocket, *, initiator_id: int):
        await connection.send_json({
            "action": "typing",
            "data": {
                "initiator_id": initiator_id
            }
        })

    async def process(self, event: ClientDirectEvent):
        action_relationship: dict[str, Callable] = {
            "typing": self.user_typing,
        }

        action = action_relationship.get(event.type)

        if action:
            action(**event.data)








