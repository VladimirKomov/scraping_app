from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.mongo_db import mongodb_client
from app.routers.scrap_router import router


@asynccontextmanager
async def lifespan(_: FastAPI):
    await mongodb_client.connect()
    yield
    await mongodb_client.close()


app = FastAPI(title="Ingredient Price API", lifespan=lifespan)

app.include_router(router)
