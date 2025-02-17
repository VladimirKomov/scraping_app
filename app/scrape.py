import asyncio

from app.config.logger_config import LoggerConfig
from app.config.config import Config
from app.db.mongo_db import mongodb_client
from app.services.scrap_service import ScrapService

logger = LoggerConfig.get_logger()

async def run_scraping():
    logger.info("Connecting to MongoDB...")
    await mongodb_client.connect()

    db = await mongodb_client.get_client()
    database = db[Config.MONGO_DB_NAME]

    service = ScrapService(database)
    await service.start_scraping()

    logger.info("Scraping completed. Closing MongoDB connection.")
    await mongodb_client.close()

if __name__ == "__main__":
    asyncio.run(run_scraping())
