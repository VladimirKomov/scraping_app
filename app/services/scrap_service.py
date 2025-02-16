import requests
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import PyMongoError

from app.api.kroger_api_client import KrogerAPIClient
from app.config.config import Config
from app.config.logger_config import LoggerConfig
from app.models.models import ScrapRequest, ScrapResponse
from app.repositories.mongo_repository import MongoRepository

logger = LoggerConfig.get_logger()


class ScrapService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.repository = MongoRepository(db)

    async def get_ingredients(self, request: ScrapRequest) -> ScrapResponse:
        """
        Gets the ingredients from the API, saves them to the database, and returns the number of records.
        """
        try:
            # Step 1: Getting ingredients from the API
            logger.info(f"Fetching ingredients for {request.ingredient} from Kroger API...")
            kroger_client = KrogerAPIClient(request.ingredient, Config.KROGER_API_LOCATION_ID)
            ingredients = await kroger_client.fetch_all_products_with_pagination()

            if not ingredients:
                logger.warning(f"No ingredients found for {request.ingredient}")
                return ScrapResponse(number_records=0)

            # Step 2: Saving it to the database
            count = await self.repository.save_ingredients(ingredients, request.ingredient, request.source_id)
            logger.info(f"Saved {count} ingredients for '{request.ingredient}' (source: {request.source_id})")

            return ScrapResponse(number_records=count)

        except requests.RequestException as e:
            logger.error(f"Kroger API error: {e}")
            raise HTTPException(status_code=502, detail="Failed to fetch ingredients from Kroger API")

        except PyMongoError as e:
            logger.error(f"MongoDB error: {e}")
            raise HTTPException(status_code=500, detail="Database error")

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
