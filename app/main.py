from fastapi import FastAPI

from app.scraping_service import process_search

app = FastAPI()

# launching the app
if __name__ == "__main__":
    # "addressLine1":"14221 E Sam Houston Pkwy N","city":"Houston"
    for i in range(10):
        process_search("03400128")
