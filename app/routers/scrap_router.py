from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.db_dependencies import get_mongo_database
from app.services.scrap_service import SpoonacularScrapService

router = APIRouter()

@router.post("/scrap-ingredients")
async def scrap_spoonacular_ingredients(
        db: AsyncIOMotorDatabase = Depends(get_mongo_database)
):
    service = SpoonacularScrapService(db)
    await service.start_scraping()
    return {"message": "Scraping completed!"}
