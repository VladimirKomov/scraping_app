from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.mongo_db import mongodb_client
from app.routers.logs_router import router as logs_router

from app.routers.scrap_router import router


@asynccontextmanager
async def lifespan(_: FastAPI):
    await mongodb_client.connect()
    yield
    await mongodb_client.close()


app = FastAPI(title="Ingredient Price API", lifespan=lifespan)

app.include_router(router, prefix="/api/v1")
app.include_router(logs_router, prefix="/ws")
