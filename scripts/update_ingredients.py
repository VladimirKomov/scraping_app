import os
import time
from datetime import datetime

import faiss
import numpy as np
from dotenv import load_dotenv
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

load_dotenv()
DATA_SOURCE = os.getenv("DATA_SOURCE")

# Connect to MongoDB
client = MongoClient("mongodb://admin:password@localhost:27017/")
db = client["kroger_db"]
products_collection = db["products_store_03400128"]
ingredients_collection = db["ingredients_cache"]

# Load SentenceTransformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Logging start of ingredient loading
print("[INFO] Starting ingredient loading from MongoDB...")

# Encode ingredient names
start_time = time.time()
ingredient_names = list(ingredients_collection.distinct("name"))
ingredient_vectors = model.encode(ingredient_names, batch_size=64, convert_to_numpy=True)

# Convert to float32 for FAISS
ingredient_vectors = np.array(ingredient_vectors, dtype=np.float32)

print(f"[INFO] Encoded {len(ingredient_names)} ingredients in {time.time() - start_time:.2f} sec.")

# Create FAISS index
start_time = time.time()
index = faiss.IndexFlatL2(ingredient_vectors.shape[1])
index.add(ingredient_vectors)
print(f"[INFO] FAISS index created in {time.time() - start_time:.2f} sec.")


def update_products():
    """Updates products by adding the most similar ingredient_name."""
    updated_count = 0

    print("[INFO] Loading products without ingredient_name...")
    start_time = time.time()

    descriptions = []
    product_ids = []

    for product in products_collection.find({"ingredient_name": {"$exists": False}}):
        description = product.get("description", "").lower().strip()
        if not description:
            continue
        descriptions.append(description)
        product_ids.append(product["_id"])

    print(f"[INFO] Loaded {len(descriptions)} products in {time.time() - start_time:.2f} sec.")

    if not descriptions:
        print("[WARNING] No products to update. Exiting.")
        return

    # Encode all descriptions in batches
    print("[INFO] Encoding product descriptions...")
    start_time = time.time()
    product_vectors = model.encode(descriptions, batch_size=64, convert_to_numpy=True)

    # Convert to float32 for FAISS
    product_vectors = np.array(product_vectors, dtype=np.float32)

    print(f"[INFO] Encoded {len(product_vectors)} products in {time.time() - start_time:.2f} sec.")

    # Find the closest ingredient using FAISS
    print("[INFO] Finding the most similar ingredients...")
    start_time = time.time()

    # Ensure product_vectors has the correct shape for FAISS
    if len(product_vectors.shape) == 1:
        product_vectors = product_vectors.reshape(1, -1)

    D, I = index.search(product_vectors, 1)
    print(f"[INFO] Found the most similar ingredients in {time.time() - start_time:.2f} sec.")

    # Update MongoDB
    print("[INFO] Updating MongoDB...")
    start_time = time.time()

    for i, product_id in enumerate(product_ids):
        best_match = ingredient_names[I[i][0]]

        products_collection.update_one(
            {"_id": product_id},
            {"$set": {
                "ingredient_name": best_match,
                "date": datetime.now(),
                "source_id": DATA_SOURCE
            }}
        )
        updated_count += 1

        # Log progress every 10,000 records
        if updated_count % 10000 == 0:
            print(f"[INFO] Processed {updated_count}/{len(product_ids)} products...")

    print(f"[INFO] Updated {updated_count} products in {time.time() - start_time:.2f} sec.")


# Run the script manually
if __name__ == "__main__":
    print("[INFO] Starting ingredient update...")
    total_start_time = time.time()
    update_products()
    print(f"[INFO] Update completed. Total execution time: {time.time() - total_start_time:.2f} sec.")
