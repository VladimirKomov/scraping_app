import asyncio
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import PyMongoError
from fastapi import HTTPException

from app.api.kroger_api_client import KrogerAPIClient
from app.api.spoonacular_api_client import SpoonacularAPIClient
from app.config.logger_config import LoggerConfig
from app.repositories.mongo_repository import MongoRepository

logger = LoggerConfig.get_logger()




class SpoonacularScrapService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.repository = MongoRepository(db)
        self.spoonacular_client = SpoonacularAPIClient()

    async def start_scraping(self):
        logger.info("Starting Spoonacular scraping process...")
        ingredients = await self.fetch_ingredients_from_spoonacular()

        if not ingredients:
            logger.warning("No ingredients found. Stopping process.")
            return

        await self.process_ingredients(ingredients)

    async def fetch_ingredients_from_spoonacular(self) -> set:
        try:
            logger.info("Fetching random recipes from Spoonacular API...")
            recipe_data = await self.spoonacular_client.fetch_random_recipe()

            if not recipe_data or "recipes" not in recipe_data:
                logger.warning("No recipes found.")
                return set()

            ingredients = set()
            for recipe in recipe_data["recipes"]:
                for ingredient in recipe.get("extendedIngredients", []):
                    ingredients.add(ingredient["name"])

            logger.info(f"Extracted {len(ingredients)} unique ingredients.")
            return ingredients

        except HTTPException as e:
            logger.error(f"API error: {e.detail}")
            raise e

        except Exception as e:
            logger.error(f"Unexpected error while fetching ingredients: {e}")
            raise HTTPException(status_code=500, detail="Error fetching ingredients from Spoonacular")

    async def process_ingredients(self, ingredients: set):
        tasks = [self.fetch_from_kroger_and_save(ingredient) for ingredient in ingredients]
        await asyncio.gather(*tasks)

    async def fetch_from_kroger_and_save(self, ingredient_name: str):
        try:
            logger.info(f"Fetching ingredient '{ingredient_name}' from Kroger API...")
            kroger_client = KrogerAPIClient(ingredient_name, "default_location")
            products = await kroger_client.fetch_all_products_with_pagination()

            if not products:
                logger.warning(f"⚠ No products found for '{ingredient_name}'. Skipping.")
                return

            await self.save_to_database(products, ingredient_name)

        except Exception as e:
            logger.error(f"Error processing ingredient '{ingredient_name}': {e}")

    async def save_to_database(self, products: list, ingredient_name: str):
        try:
            count = await self.repository.save_ingredients(products, ingredient_name, "spoonacular")
            logger.info(f"Successfully saved {count} products for '{ingredient_name}'.")

        except PyMongoError as e:
            logger.error(f"MongoDB error while saving '{ingredient_name}': {e}")
            raise HTTPException(status_code=500, detail="Database error while saving data")
