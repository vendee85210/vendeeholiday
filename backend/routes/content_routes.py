from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List

from models import InspirationCategory, SpecialOffer
from database import get_database

router = APIRouter(prefix="/api", tags=["content"])

@router.get("/inspiration", response_model=List[InspirationCategory])
async def get_inspiration_categories(
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get all inspiration categories"""
    categories_data = await db.inspiration_categories.find({}).to_list(None)
    
    # Update property counts for each category
    categories = []
    for cat_data in categories_data:
        # Count properties that match this category
        # This is a simplified matching - in real implementation, 
        # you'd have proper category-to-property relationships
        property_count = await db.properties.count_documents({"is_active": True})
        
        cat_data["property_count"] = property_count // 4  # Distribute roughly
        categories.append(InspirationCategory(**cat_data))
    
    return categories

@router.get("/special-offers", response_model=List[SpecialOffer])
async def get_special_offers(
    active_only: bool = True,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get current special offers"""
    from datetime import datetime
    
    filter_query = {}
    if active_only:
        filter_query.update({
            "active": True,
            "valid_from": {"$lte": datetime.utcnow()},
            "valid_until": {"$gte": datetime.utcnow()}
        })
    
    offers_data = await db.special_offers.find(filter_query).to_list(None)
    return [SpecialOffer(**offer) for offer in offers_data]