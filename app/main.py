from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
import uvicorn
from app.scraping_service import process_search
import sys
import os
import asyncio

app = FastAPI()

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
    for i in range(10):
        process_search("03400128")
    return {"status": "success"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


# launching the app
# if __name__ == "__main__":
#     # "addressLine1":"14221 E Sam Houston Pkwy N","city":"Houston"
#     for i in range(10):
#         process_search("03400128")
