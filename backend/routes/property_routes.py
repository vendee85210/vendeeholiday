from fastapi import APIRouter, Depends, HTTPException, status, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional
from datetime import datetime, date

from models import (
    Property, PropertyCreate, PropertyUpdate, PropertyResponse,
    PropertySearchFilters, SearchResponse, User, UserRole
)
from auth import get_current_active_user
from database import get_database

router = APIRouter(prefix="/api/properties", tags=["properties"])

@router.get("", response_model=List[Property])
async def list_properties(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    region: Optional[str] = None,
    property_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """List all active properties with optional filters"""
    filter_query = {"is_active": True}
    
    # Apply filters
    if region:
        filter_query["location.region"] = {"$regex": region, "$options": "i"}
    if property_type:
        filter_query["property_type"] = property_type
    if min_price is not None:
        filter_query["price_per_night"] = {"$gte": min_price}
    if max_price is not None:
        if "price_per_night" in filter_query:
            filter_query["price_per_night"]["$lte"] = max_price
        else:
            filter_query["price_per_night"] = {"$lte": max_price}
    
    # Fetch properties
    cursor = db.properties.find(filter_query).skip(skip).limit(limit)
    properties_data = await cursor.to_list(limit)
    
    return [Property(**prop) for prop in properties_data]

@router.get("/search", response_model=SearchResponse)
async def search_properties(
    region: Optional[str] = None,
    check_in: Optional[date] = None,
    check_out: Optional[date] = None,
    guests: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    property_type: Optional[str] = None,
    bedrooms: Optional[int] = None,
    amenities: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Advanced property search with availability checking"""
    filter_query = {"is_active": True}
    
    # Apply basic filters
    if region:
        filter_query["location.region"] = {"$regex": region, "$options": "i"}
    if property_type:
        filter_query["property_type"] = property_type
    if guests:
        filter_query["max_guests"] = {"$gte": guests}
    if bedrooms:
        filter_query["bedrooms"] = {"$gte": bedrooms}
    if min_price is not None:
        filter_query["price_per_night"] = {"$gte": min_price}
    if max_price is not None:
        if "price_per_night" in filter_query:
            filter_query["price_per_night"]["$lte"] = max_price
        else:
            filter_query["price_per_night"] = {"$lte": max_price}
    
    # Parse amenities if provided
    if amenities:
        amenity_list = [a.strip() for a in amenities.split(",")]
        filter_query["amenities"] = {"$in": amenity_list}
    
    # Check availability if dates provided
    if check_in and check_out:
        # Find properties that don't have conflicting bookings
        conflicting_bookings = await db.bookings.find({
            "status": {"$in": ["confirmed", "pending"]},
            "$or": [
                {"check_in": {"$lte": check_out}, "check_out": {"$gte": check_in}}
            ]
        }).to_list(None)
        
        booked_property_ids = [booking["property_id"] for booking in conflicting_bookings]
        if booked_property_ids:
            filter_query["id"] = {"$nin": booked_property_ids}
    
    # Get total count
    total_count = await db.properties.count_documents(filter_query)
    
    # Fetch properties
    cursor = db.properties.find(filter_query).skip(skip).limit(limit)
    properties_data = await cursor.to_list(limit)
    properties = [Property(**prop) for prop in properties_data]
    
    # Create filters object
    filters = PropertySearchFilters(
        region=region,
        check_in=check_in,
        check_out=check_out,
        guests=guests,
        min_price=min_price,
        max_price=max_price,
        property_type=property_type,
        bedrooms=bedrooms,
        amenities=amenities.split(",") if amenities else None
    )
    
    return SearchResponse(
        properties=properties,
        total_count=total_count,
        filters_applied=filters
    )

@router.get("/{property_id}", response_model=PropertyResponse)
async def get_property(
    property_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get single property by ID"""
    property_data = await db.properties.find_one({"id": property_id, "is_active": True})
    if not property_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    property_obj = Property(**property_data)
    
    # Get owner info (optional)
    owner_data = await db.users.find_one({"id": property_obj.owner_id})
    owner = None
    if owner_data:
        from models import UserResponse
        owner = UserResponse(
            id=owner_data["id"],
            email=owner_data["email"],
            first_name=owner_data["first_name"],
            last_name=owner_data["last_name"],
            role=owner_data["role"],
            created_at=owner_data["created_at"]
        )
    
    return PropertyResponse(**property_obj.dict(), owner=owner)

@router.post("", response_model=Property)
async def create_property(
    property_data: PropertyCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Create new property (owners and admins only)"""
    if current_user.role not in [UserRole.owner, UserRole.admin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only property owners can create properties"
        )
    
    property_obj = Property(**property_data.dict(), owner_id=current_user.id)
    await db.properties.insert_one(property_obj.dict())
    
    return property_obj

@router.put("/{property_id}", response_model=Property)
async def update_property(
    property_id: str,
    updates: PropertyUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Update property (owner or admin only)"""
    # Get property
    property_data = await db.properties.find_one({"id": property_id})
    if not property_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    # Check ownership
    if current_user.role != UserRole.admin and property_data["owner_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own properties"
        )
    
    # Prepare update data
    update_data = {}
    for field, value in updates.dict(exclude_unset=True).items():
        if value is not None:
            update_data[field] = value
    
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
        await db.properties.update_one(
            {"id": property_id},
            {"$set": update_data}
        )
    
    # Return updated property
    updated_data = await db.properties.find_one({"id": property_id})
    return Property(**updated_data)

@router.delete("/{property_id}")
async def delete_property(
    property_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Delete property (soft delete by setting inactive)"""
    # Get property
    property_data = await db.properties.find_one({"id": property_id})
    if not property_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    # Check ownership
    if current_user.role != UserRole.admin and property_data["owner_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own properties"
        )
    
    # Soft delete
    await db.properties.update_one(
        {"id": property_id},
        {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
    )
    
    return {"message": "Property deleted successfully"}