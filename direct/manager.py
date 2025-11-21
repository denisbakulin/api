from functools import wraps
from typing import Optional

from fastapi import WebSocket


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









