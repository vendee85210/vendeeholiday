from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List

from models import Destination, Property
from database import get_database

router = APIRouter(prefix="/api/destinations", tags=["destinations"])

@router.get("", response_model=List[Destination])
async def list_destinations(
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get all destinations"""
    destinations_data = await db.destinations.find({}).to_list(None)
    
    # Update property counts
    destinations = []
    for dest_data in destinations_data:
        # Count active properties in this region
        property_count = await db.properties.count_documents({
            "location.region": {"$regex": dest_data["name"], "$options": "i"},
            "is_active": True
        })
        
        dest_data["property_count"] = property_count
        destinations.append(Destination(**dest_data))
    
    return destinations

@router.get("/{slug}", response_model=Destination)
async def get_destination(
    slug: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get destination by slug"""
    destination_data = await db.destinations.find_one({"slug": slug})
    if not destination_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination not found"
        )
    
    # Update property count
    property_count = await db.properties.count_documents({
        "location.region": {"$regex": destination_data["name"], "$options": "i"},
        "is_active": True
    })
    destination_data["property_count"] = property_count
    
    return Destination(**destination_data)

@router.get("/{slug}/properties", response_model=List[Property])
async def get_destination_properties(
    slug: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get all properties in a destination"""
    # Get destination
    destination_data = await db.destinations.find_one({"slug": slug})
    if not destination_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination not found"
        )
    
    # Get properties in this region
    properties_data = await db.properties.find({
        "location.region": {"$regex": destination_data["name"], "$options": "i"},
        "is_active": True
    }).to_list(None)
    
    return [Property(**prop) for prop in properties_data]