from motor.motor_asyncio import AsyncIOMotorDatabase

from app.config.config import Config
from app.db.mongo_db import mongodb_client


async def get_mongo_database() -> AsyncIOMotorDatabase:
    client = await mongodb_client.get_client()
    return client[Config.MONGO_DB_NAME]