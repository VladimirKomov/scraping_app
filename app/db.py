from pymongo import MongoClient

from app import config

# Connect to MongoDB
MONGO_URI = config.MONGO_URI
DB_NAME = "kroger_db"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def get_ingredient_collection():
    return db["ingredients_cache"]

def get_store_collection(store_id):
    return db[f"products_store_{store_id}"]
