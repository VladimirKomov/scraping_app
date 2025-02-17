import httpx
import asyncio

from app.config.config import Config
from app.config.logger_config import LoggerConfig


logger = LoggerConfig.get_logger()


class SpoonacularAPIClient:
    """Client for interacting with the Spoonacular API."""

    SPOONACULAR_API_BASE_URL = Config.SPOONACULAR_API_BASE_URL
    SPOONACULAR_API_KEYS = Config.SPOONACULAR_API_KEYS
    _current_key_index = 0

    async def _get_random_recipe(self):
        """Fetches random recipes asynchronously from the Spoonacular API."""
        for _ in range(len(self.SPOONACULAR_API_KEYS)):
            api_key = self.SPOONACULAR_API_KEYS[self._current_key_index]

            async with httpx.AsyncClient(timeout=10) as client:
                try:
                    response = await client.get(
                        f"{self.SPOONACULAR_API_BASE_URL}/recipes/random",
                        params={
                            "apiKey": api_key,
                            "number": 100,
                        },
                    )

                    if response.status_code in [402, 429]:
                        logger.warning(f"API key {api_key} exceeded rate limit. Trying another key.")
                        self._switch_api_key()
                        await asyncio.sleep(2)
                        continue

                    response.raise_for_status()
                    return response.json()

                except httpx.HTTPError as e:
                    logger.error(f"Request error while fetching recipes: {e}")
                    raise Exception(f"Request error while fetching recipes: {e}")

        logger.error("All API keys have exceeded their limits or failed.")
        raise Exception("No valid API key available.")

    def _switch_api_key(self):
        """Switches to the next available API key."""
        self._current_key_index = (self._current_key_index + 1) % len(self.SPOONACULAR_API_KEYS)

    def fetch_random_recipe(self):
        """Fetches a random recipe using the external function."""
        return self._get_random_recipe()
