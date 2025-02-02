"""
This module is specific to the Kroger API.
It handles authentication by obtaining and caching an access token
required for making authorized requests to the Kroger API.
"""

import base64
import requests
import time
from app.config import KROGER_CLIENT_ID, KROGER_CLIENT_SECRET, KROGER_TOKEN_URL

# Global variables for storing the token and its expiration time
token_cache = {"access_token": None, "expires_at": 0}

def get_kroger_token():
    current_time = time.time()

    # Check if the token exists and is still valid
    if token_cache["access_token"] and token_cache["expires_at"] > current_time:
        return token_cache["access_token"]

    # If the token is missing or expired, request a new one
    credentials = base64.b64encode(f"{KROGER_CLIENT_ID}:{KROGER_CLIENT_SECRET}".encode()).decode()
    response = requests.post(
        KROGER_TOKEN_URL,
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data={"grant_type": "client_credentials", "scope": "product.compact"}
    )

    if response.status_code == 200:
        token_data = response.json()
        token_cache["access_token"] = token_data["access_token"]
        token_cache["expires_at"] = current_time + token_data["expires_in"]  # Store expiration time
        return token_data["access_token"]
    else:
        raise Exception(f"Failed to get access token: {response.text}")
