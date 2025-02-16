import os

from dotenv import load_dotenv

from app.config.logger_config import LoggerConfig

# Loading environment variables from .env
load_dotenv()

logger = LoggerConfig.get_logger()


class Config:
    MONGO_URL = os.getenv("MONGO_URL")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
    MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME")

    KROGER_API_BASE_URL = os.getenv("KROGER_API_BASE_URL")
    KROGER_API_TOKEN_URL = os.getenv("KROGER_API_TOKEN_URL")
    KROGER_API_CLIENT_ID = os.getenv("KROGER_API_CLIENT_ID")
    KROGER_API_CLIENT_SECRET = os.getenv("KROGER_API_CLIENT_SECRET")
    KROGER_API_LOCATION_ID = os.getenv("KROGER_API_LOCATION_ID")

    SPOONACULAR_API_BASE_URL = os.getenv("SPOONACULAR_API_BASE_URL", "https://api.spoonacular.com/")
    SPOONACULAR_API_KEYS = [key.strip() for key in (os.getenv("SPOONACULAR_API_KEYS") or "").split(",") if key.strip()]

    REQUIRED_VARS = {
        "MONGO_URL": MONGO_URL,
        "MONGO_DB_NAME": MONGO_DB_NAME,
        "MONGO_COLLECTION_NAME": MONGO_COLLECTION_NAME,
        "KROGER_API_BASE_URL": KROGER_API_BASE_URL,
        "KROGER_API_TOKEN_URL": KROGER_API_TOKEN_URL,
        "KROGER_API_CLIENT_ID": KROGER_API_CLIENT_ID,
        "KROGER_API_CLIENT_SECRET": KROGER_API_CLIENT_SECRET,
        "KROGER_API_LOCATION_ID": KROGER_API_LOCATION_ID,
        "SPOONACULAR_API_BASE_URL": SPOONACULAR_API_BASE_URL,
        "SPOONACULAR_API_KEYS": SPOONACULAR_API_KEYS,
    }

    missing_vars = [var for var, value in REQUIRED_VARS.items() if not value]

    if missing_vars:
        logger.error(f"ERROR: Missing required environment variables: {', '.join(missing_vars)}")
        raise ValueError(f"ERROR: Missing required environment variables: {', '.join(missing_vars)}")
