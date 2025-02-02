import requests
from pymongo import MongoClient

from app.config import SPOONACULAR_API_KEY
from app.kroger_service import fetch_all_products_with_pagination

# Connect to MongoDB
client = MongoClient("mongodb://admin:password@localhost:27017/")
db = client["kroger_db"]
ingredients_collection = db["ingredients_cache"]


def get_existing_ingredients():
    """Retrieves a list of ingredients that have already been queried."""
    return set(ingredients_collection.distinct("name"))


def get_random_recipe():
    """Fetches a random recipe from the Spoonacular API."""
    url = f"https://api.spoonacular.com/recipes/random?apiKey={SPOONACULAR_API_KEY}&number=1"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json().get("recipes", [])
        if not data:
            print("❌ Error: Spoonacular returned an empty recipe list.")
            return None, []

        recipe = data[0]
        title = recipe["title"]
        ingredients = {ingredient["name"].lower() for ingredient in recipe["extendedIngredients"]}

        print(f"\n🍽️ Random Recipe: {title}")
        print("🛒 Ingredients:")
        for ing in ingredients:
            print(f"  - {ing}")

        return title, ingredients

    print(f"❌ Error fetching data from Spoonacular API: {response.status_code}")
    return None, []


def find_new_ingredients(ingredients):
    """Determines which ingredients have not yet been queried in API."""
    existing_ingredients = get_existing_ingredients()
    return [ing for ing in ingredients if ing not in existing_ingredients]


def save_ingredient_to_db(ingredient):
    """Saves an ingredient to the database if it does not already exist."""
    try:
        ingredients_collection.update_one(
            {"name": ingredient},
            {"$setOnInsert": {"name": ingredient}},
            upsert=True
        )
        print(f"✅ Ingredient saved to the database: {ingredient}")
    except Exception as e:
        print(f"❌ Error saving '{ingredient}': {e}")


def process_search(location_id: str):
    """
    Loads a list of new ingredients, queries them in API,
    and saves the results to the database.
    """
    title, ingredients = get_random_recipe()
    if not ingredients:
        print("❌ Error: Failed to retrieve ingredients.")
        return

    new_ingredients = find_new_ingredients(ingredients)
    if not new_ingredients:
        print("\n✅ All ingredients are already in the database, no API query required.")
        return

    print("\n🔍 Starting price search in API...")
    for ingredient in new_ingredients:
        try:
            print(f"\n🛒 Querying products for: {ingredient}...")
            products = fetch_all_products_with_pagination(ingredient, location_id)

            if products:
                print(f"✅ Found {len(products)} products for '{ingredient}', saving to database.")
                save_ingredient_to_db(ingredient)
            else:
                print(f"❌ No products found for '{ingredient}'.")

        except Exception as e:
            print(f"❌ Error querying '{ingredient}': {e}")
