import asyncio
import logging
from fastapi import WebSocket
from typing import List

connected_websockets: List[WebSocket] = []

class WebSocketLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()

    async def send_to_websockets(self, message: str):
        for ws in connected_websockets:
            try:
                await ws.send_text(message)
            except Exception as e:
                print(f"WebSocket error: {e}")

    def emit(self, record: logging.LogRecord):
        message = self.format(record)
        asyncio.create_task(self.send_to_websockets(message))
