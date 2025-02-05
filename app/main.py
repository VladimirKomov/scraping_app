from fastapi import FastAPI

from app.db import mongo_db
from app.scraping_service import process_search

app = FastAPI()

# launching the app
if __name__ == "__main__":
    print("🚀 Running data processing manually...")
    try:
        for i in range(10):
            process_search("03400128")
    except Exception as e:
        print(f"❌ Error during processing: {e}")
    finally:
        print("🔴 Closing processing...")
        mongo_db.client.close()
