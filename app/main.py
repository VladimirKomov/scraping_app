import asyncio
import os
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles

from app.db import mongo_db
from app.scraping_service import process_search


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n🚀 Starting FastAPI app...")
    yield
    print("🔴 Closing MongoDB connection...")
    mongo_db.client.close()


app = FastAPI(lifespan=lifespan)

# Defining the path to the static folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Connect the static folder so that FastAPI distributes static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

connected_clients = []


# Function for intercepting print() and sending it to WebSocket
class WebSocketLogger:
    def write(self, message):
        if message.strip():
            for client in connected_clients:
                try:
                    asyncio.run(client.send_text(message))
                except:
                    pass

    def flush(self):
        pass


# Overloading print() in WebSocketLogger
sys.stdout = WebSocketLogger()


# WebSocket endpoint for logs
@app.websocket("/logs")
async def websocket_logs(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        pass
    finally:
        connected_clients.remove(websocket)


# endpoint for launching `process_search`
@app.post("/run_process")
def run_process():
    # "addressLine1":"14221 E Sam Houston Pkwy N","city":"Houston"
    print("🚀 Starting processing...")
    try:
        for i in range(10):
            process_search("03400128")
    except Exception as e:
        print(f"❌   Error during processing: {e}")
    finally:
        total_records = mongo_db.get_total_products("03400128")
        print(f"📊 Total records in database: {total_records}")
        print("🎯 Closing processing...")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
