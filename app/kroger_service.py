"""
This module is the primary handler for retrieving and saving product data from the Kroger API.
It connects to MongoDB and dynamically stores product information per store.
"""
from datetime import datetime
import random
import time

import requests
from pymongo import MongoClient
from app.auth import get_kroger_token
from app.config import BASE_URL, DATA_SOURCE, MONGO_URI

# Connect to MongoDB
client = MongoClient(MONGO_URI)
# you can replace the name with any of your own
db = client["kroger_db"]

def save_response_to_store_collection(response, store_id, keyword):
    """
    Saves the API response data to a dynamically created MongoDB collection for a specific store.

    :param response: API response containing product data.
    :param store_id: Unique store identifier.
    """
    if "data" not in response:
        print(f"No data to save for store {store_id}.")
        return

    store_collection = db[f"products_store_{store_id}"]
    products = response["data"]  # Retrieve product list

    for product in products:
        try:
            # Add mandatory fields
            product["ingredient_name"] = keyword
            product["date"] = datetime.now()
            product["data_source"] = DATA_SOURCE

            # Use upsert to avoid duplicates
            store_collection.update_one(
                # Unique identifier: productId
                {"productId": product["productId"]},
                # Update or insert data
                {"$set": product},
                upsert=True
            )
        except Exception as e:
            print(f"Error saving product {product.get('productId', 'UNKNOWN')} in store {store_id}: {e}")

    print(f"Saved {len(products)} products to collection products_store_{store_id}.")


def fetch_all_products_with_pagination(keyword: str, location_id: str):
    """
    Fetches products from the Kroger API using pagination and stores the results in MongoDB.

    :param keyword: Search term for products.
    :param location_id: Store location ID.
    :return: List of retrieved products.
    """
    token = get_kroger_token()
    # Store all retrieved products
    all_products = []
    # Track unique product IDs
    seen_product_ids = set()
    # Start index (0 is not allowed)
    start = 1
    # Maximum limit per request
    limit = 50

    while True:
        # the function of falling asleep
        delay = random.uniform(1, 5)
        print(f"Sleeping for {delay:.2f} seconds... start = {start}")
        time.sleep(delay)
        print("Proceeding!")

        if start > 250:
            break

        # response
        response = requests.get(
            f"{BASE_URL}products",
            headers={"Authorization": f"Bearer {token}"},
            params={
                "filter.term": keyword,
                "filter.locationId": location_id,
                "filter.start": start,
                "filter.limit": limit,
            },
            timeout=10
        )

        if response.status_code != 200:
            raise Exception(f"Failed to fetch products: {response.text}")

        response_data = response.json()
        products = response_data.get("data", [])
        if not products:
            # Exit loop if no more products
            break

        # Add only unique products
        for product in products:
            if product["productId"] not in seen_product_ids:
                all_products.append(product)
                seen_product_ids.add(product["productId"])

        # Save the current batch of products to the database
        save_response_to_store_collection({"data": products}, location_id, keyword)

        # Increase the offset
        start += limit

        # Check the total available results
        if "meta" in response_data and "pagination" in response_data["meta"]:
            total = response_data["meta"]["pagination"]["total"]
            if start > total:
                break
            if start > 251:
                break

    print(f"Total products retrieved: {len(all_products)}")
    return all_products
