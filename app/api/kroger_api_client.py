import asyncio
import base64
import json
import time

import httpx

print(f"Imported httpx in: {__name__}")

from app.config.config import Config
from app.config.logger_config import LoggerConfig

logger = LoggerConfig.get_logger()


class KrogerAPIClient:
    # Load API configuration from Config
    KROGER_API_BASE_URL = Config.KROGER_API_BASE_URL
    KROGER_API_TOKEN_URL = Config.KROGER_API_TOKEN_URL
    KROGER_API_CLIENT_ID = Config.KROGER_API_CLIENT_ID
    KROGER_API_CLIENT_SECRET = Config.KROGER_API_CLIENT_SECRET

    # Global Token Cache
    token_cache = {"access_token": None, "expires_at": 0}
    _token_lock = asyncio.Lock()

    def __init__(self, keyword: str, location_id: str = None):
        """
        Initializing a client to receive products from the Kroger API.

        :param keyword: Search query.
        :param location_id: The store's ID.
        """
        self.keyword = keyword
        self.location_id = location_id or Config.KROGER_API_LOCATION_ID
        self.seen_product_ids = set()
        self.all_products = []
        # Pagination start index
        self.start = 1
        # Max items per request
        self.limit = 50

    @classmethod
    async def _get_kroger_token(cls):
        """Fetches a token from the Kroger API using caching."""

        async with cls._token_lock:
            current_time = time.time()
            # Return cached token if still valid
            if cls.token_cache["access_token"] and cls.token_cache["expires_at"] > current_time:
                return cls.token_cache["access_token"]

            # If the token is missing or expired, request a new one
            credentials = base64.b64encode(
                f"{cls.KROGER_API_CLIENT_ID}:{cls.KROGER_API_CLIENT_SECRET}".encode()).decode()

            async with httpx.AsyncClient(timeout=10) as client:
                try:
                    response = await client.post(
                        cls.KROGER_API_TOKEN_URL,
                        headers={
                            "Authorization": f"Basic {credentials}",
                            "Content-Type": "application/x-www-form-urlencoded"
                        },
                        data={"grant_type": "client_credentials", "scope": "product.compact"},
                    )

                    if response.status_code == 200:
                        try:
                            token_data = await response.json()
                        except Exception as e:
                            logger.error(f"Invalid JSON response: {e}")
                            raise Exception(f"Invalid JSON response: {e}")
                        cls.token_cache["access_token"] = token_data.get("access_token")
                        cls.token_cache["expires_at"] = current_time + token_data.get("expires_in", 0)
                        return token_data["access_token"]
                    else:
                        logger.error(f"Failed to get access token: {response.text}")
                        raise Exception(f"Failed to get access token: {response.text}")

                except httpx.HTTPError as e:
                    logger.error(f"Request error while fetching token: {e}")
                    raise Exception(f"Request error while fetching token: {e}")

    async def _get_products(self):
        """Executes a request to the Kroger API."""

        # Always use the latest token
        token = await self._get_kroger_token()

        async with httpx.AsyncClient(timeout=10) as client:
            try:
                response = await client.get(
                    f"{self.KROGER_API_BASE_URL}products",
                    headers={"Authorization": f"Bearer {token}"},
                    params={
                        "filter.term": self.keyword,
                        "filter.locationId": self.location_id,
                        "filter.start": self.start,
                        "filter.limit": self.limit,
                    },
                )

                if response.status_code != 200:
                    logger.error(f"Failed to fetch products: {response.text}")
                    raise Exception(f"Failed to fetch products: {response.text}")

                try:
                    return await response.json()
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON response: {e}")
                    raise Exception(f"Invalid JSON response: {e}")

            except httpx.HTTPError as e:
                logger.error(f"Request error while fetching products: {e}")
                raise Exception(f"Request error while fetching products: {e}")

    async def fetch_all_products_with_pagination(self):
        """Fetches products from the Kroger API using asynchronous pagination."""
        while True:
            if self.start > 250:
                break

            response_data = await self._get_products()
            products = response_data.get("data", [])

            if not products:
                logger.info("No more products found, stopping pagination.")
                break

            for product in products:
                if product["productId"] not in self.seen_product_ids:
                    self.all_products.append(product)
                    self.seen_product_ids.add(product["productId"])

            # Increase offset
            self.start += self.limit

            if "meta" in response_data and "pagination" in response_data["meta"]:
                total = response_data["meta"]["pagination"].get("total", 0)
                if self.start >= total:
                    break

        logger.info(f"Total products retrieved: {len(self.all_products)}")
        return self.all_products
