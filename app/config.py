import os
from dotenv import load_dotenv

"""
This is the main configuration file for API access.
"""

# Load environment variables from .env file
load_dotenv()

# Main api URL
BASE_URL = os.getenv("BASE_URL")

# Very important number from the file
DATA_SOURCE = os.getenv("DATA_SOURCE")

# I use an API with mandatory additional authorization, configurations may differ for other APIs.
KROGER_CLIENT_ID = os.getenv("KROGER_CLIENT_ID")
KROGER_CLIENT_SECRET = os.getenv("KROGER_CLIENT_SECRET")
KROGER_TOKEN_URL = os.getenv("KROGER_TOKEN_URL")
SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:password@localhost:27017/")
