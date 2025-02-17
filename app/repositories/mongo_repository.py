from datetime import datetime, UTC

from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import PyMongoError

from app.config.config import Config
from app.config.logger_config import LoggerConfig

logger = LoggerConfig.get_logger()


class MongoRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.products_collection = db[Config.MONGO_COLLECTION_NAME]

    async def save_ingredients(self, ingredients: list, ingredient_name: str, source_id: str) -> int:
        """
        Saves ingredients to MongoDB.

        :param ingredients: List of ingredients.
        :param ingredient_name: Name of the ingredient.
        :param source_id: Data source ID.
        :return: Number of records saved.
        """
        try:
            if not ingredients:
                return 0

            # Add metadata
            for item in ingredients:
                item["ingredient_name"] = ingredient_name
                item["date"] = datetime.now(UTC)
                item["source_id"] = source_id

            result = await self.products_collection.insert_many(ingredients)
            count = len(result.inserted_ids)
            logger.info(f"Inserted {count} records for ingredient '{ingredient_name}' from source '{source_id}'")
            return count

        except PyMongoError as e:
            logger.error(f"MongoDB save error: {e}")
            raise
