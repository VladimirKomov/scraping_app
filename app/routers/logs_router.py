from fastapi import APIRouter, WebSocket
import asyncio
from typing import List

from app.config.logger_config import LoggerConfig
from app.handlers.web_socket_handler import connected_websockets

logger = LoggerConfig.get_logger()

router = APIRouter()

@router.websocket("/logs")
async def websocket_logs(websocket: WebSocket):
    await websocket.accept()
    connected_websockets.append(websocket)
    try:
        while True:
            await asyncio.sleep(0.1)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        connected_websockets.remove(websocket)
