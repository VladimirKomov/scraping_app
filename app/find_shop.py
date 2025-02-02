"""
This module is specific to the Kroger API.
It processes a JSON file containing store data and filters Kroger stores based on city and state.

It allows for manual parameter configuration and supports searching in the largest U.S. cities.
"""

import json

# Manual configuration parameters
FILENAME = "Kroger.json"
CITY = ""
STATE = ""
LARGEST_CITIES = ["Los Angeles", "Houston", "Chicago", "Phoenix", "Philadelphia",
                  "San Antonio", "San Diego", "Dallas", "San Jose", "Austin"]

def find_kroger_stores(filename, city=None, state=None, largest_cities=None):
    """
    Searches for Kroger stores in a JSON file based on city and state.

    :param filename: Path to the JSON file containing store data.
    :param city: City name (e.g., "New York"). Optional parameter.
    :param state: State code (e.g., "NY"). Optional parameter.
    :return: List of found Kroger stores.
    """
    try:
        # Load JSON file
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Filter only Kroger stores
        kroger_stores = [store for store in data["data"] if store.get("chain") == "KROGER"]

        # Filter by city if specified
        if city:
            kroger_stores = [store for store in kroger_stores if store["address"]["city"].lower() == city.lower()]

        # Filter by state if specified
        if state:
            kroger_stores = [store for store in kroger_stores if store["address"]["state"].upper() == state.upper()]

        if largest_cities:
            largest_cities_set = {city.lower() for city in largest_cities}  # Create a set of cities in lowercase
            kroger_stores = [store for store in kroger_stores if store["address"]["city"].lower() in largest_cities_set]

        # Display results
        if kroger_stores:
            print(f"\n🔎 Found {len(kroger_stores)} Kroger stores:")
            for store in kroger_stores:
                print(f"📍 {store['name']} ({store['address']['city']}, {store['address']['state']}), id: {store['locationId']}")
                print(f"   📌 Address: {store['address']['addressLine1']}, {store['address']['zipCode']}")
                print(f"   ☎️ Phone: {store.get('phone', 'Not provided')}")
                print("-" * 50)
        else:
            print("❌ No Kroger stores found.")

        return kroger_stores

    except FileNotFoundError:
        print("❌ Error: File not found.")
    except json.JSONDecodeError:
        print("❌ Error: Invalid JSON format.")

# Run script with fixed parameters
if __name__ == "__main__":
    find_kroger_stores(FILENAME, CITY, STATE, LARGEST_CITIES)
