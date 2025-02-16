from motor.motor_asyncio import AsyncIOMotorClient

from app.config.config import Config
from app.config.logger_config import LoggerConfig

logger = LoggerConfig.get_logger()


class MongoDBClient:
    _instance = None

    def __new__(cls):
        """ Singleton pattern to ensure a single MongoDB connection """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = None
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'client'):
            self.client = None

    async def connect(self) -> None:
        """ Initialize the MongoDB connection if not already connected or lost """
        if self.client is None:
            self.client = AsyncIOMotorClient(
                Config.MONGO_URL,
                serverSelectionTimeoutMS=3000
            )
            logger.info("Connected to MongoDB")
        else:
            try:
                await self.client.admin.command('ping')
            except Exception as e:
                logger.error(f"MongoDB connection lost: {e}. Reconnecting...")
                self.client.close()
                self.client = AsyncIOMotorClient(
                    Config.MONGO_URL,
                    serverSelectionTimeoutMS=3000,
                    retryWrites=False
                )
                logger.info("Reconnected to MongoDB")

    async def get_client(self) -> AsyncIOMotorClient:
        """ Returns the MongoDB client """
        await self.connect()
        return self.client

    async def close(self) -> None:
        """ Close the MongoDB connection """
        if self.client:
            try:
                self.client.close()
                logger.info("MongoDB connection closed")
            except Exception as e:
                logger.error(f"Error closing MongoDB connection: {e}")
            finally:
                self.client = None


mongodb_client = MongoDBClient()
