from fastapi import FastAPI
import uvicorn
from app.scraping_service import process_search

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}

# New endpoint for launching `process_search`
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
