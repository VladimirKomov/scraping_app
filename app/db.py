from pymongo import MongoClient
from app import config

class MongoDB:
    """A class for managing MongoDB connectivity and collections."""

    # use singleton
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)
            cls._instance._init_db()
        return cls._instance

    def _init_db(self):
        self.client = MongoClient(config.MONGO_URL)
        self.db = self.client["kroger_db"]

        self.ingredients_collection = self.db["ingredients_cache"]

    def get_store_collection(self, store_id):
        return self.db[f"products_store_{store_id}"]

    def close(self):
        self.client.close()
        MongoDB._instance = None

# Database instance (created once)
mongo_db = MongoDB()