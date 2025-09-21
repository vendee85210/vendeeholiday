from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from datetime import datetime

from models import Review, ReviewCreate, ReviewResponse, User, UserRole
from auth import get_current_active_user
from database import get_database

router = APIRouter(prefix="/api", tags=["reviews"])

@router.get("/properties/{property_id}/reviews", response_model=List[ReviewResponse])
async def get_property_reviews(
    property_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get all reviews for a property"""
    reviews_data = await db.reviews.find({
        "property_id": property_id
    }).sort("created_at", -1).to_list(None)
    
    # Enrich with user data
    reviews = []
    for review_data in reviews_data:
        review = Review(**review_data)
        
        # Get user info (without sensitive data)
        user = None
        user_data = await db.users.find_one({"id": review.user_id})
        if user_data:
            from models import UserResponse
            user = UserResponse(
                id=user_data["id"],
                email="",  # Don't expose email
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                role=user_data["role"],
                created_at=user_data["created_at"]
            )
        
        reviews.append(ReviewResponse(**review.dict(), user=user))
    
    return reviews

@router.post("/properties/{property_id}/reviews", response_model=ReviewResponse)
async def create_review(
    property_id: str,
    review_data: ReviewCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Create a new review for a property"""
    # Verify property exists
    property_data = await db.properties.find_one({"id": property_id, "is_active": True})
    if not property_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    # Check if user has a completed booking for this property
    booking = await db.bookings.find_one({
        "user_id": current_user.id,
        "property_id": property_id,
        "status": "completed"
    })
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can only review properties you have booked and stayed at"
        )
    
    # Check if user already reviewed this property
    existing_review = await db.reviews.find_one({
        "user_id": current_user.id,
        "property_id": property_id
    })
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already reviewed this property"
        )
    
    # Create review
    review = Review(
        **review_data.dict(),
        user_id=current_user.id,
        booking_id=booking["id"]
    )
    
    await db.reviews.insert_one(review.dict())
    
    # Update property average rating
    await update_property_rating(db, property_id)
    
    # Return review with user data
    from models import UserResponse
    user_response = UserResponse(
        id=current_user.id,
        email="",  # Don't expose email
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        role=current_user.role,
        created_at=current_user.created_at
    )
    
    return ReviewResponse(**review.dict(), user=user_response)

@router.get("/reviews/{review_id}", response_model=ReviewResponse)
async def get_review(
    review_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get single review by ID"""
    review_data = await db.reviews.find_one({"id": review_id})
    if not review_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    review = Review(**review_data)
    
    # Get user info
    user = None
    user_data = await db.users.find_one({"id": review.user_id})
    if user_data:
        from models import UserResponse
        user = UserResponse(
            id=user_data["id"],
            email="",  # Don't expose email
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            role=user_data["role"],
            created_at=user_data["created_at"]
        )
    
    return ReviewResponse(**review.dict(), user=user)

@router.put("/reviews/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: str,
    updates: ReviewCreate,  # Reuse ReviewCreate for updates
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Update review (author only)"""
    review_data = await db.reviews.find_one({"id": review_id})
    if not review_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    # Check ownership
    if current_user.id != review_data["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own reviews"
        )
    
    # Update review
    update_data = updates.dict()
    update_data["updated_at"] = datetime.utcnow()
    
    await db.reviews.update_one(
        {"id": review_id},
        {"$set": update_data}
    )
    
    # Update property rating
    await update_property_rating(db, review_data["property_id"])
    
    # Return updated review
    updated_data = await db.reviews.find_one({"id": review_id})
    review = Review(**updated_data)
    
    from models import UserResponse
    user_response = UserResponse(
        id=current_user.id,
        email="",
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        role=current_user.role,
        created_at=current_user.created_at
    )
    
    return ReviewResponse(**review.dict(), user=user_response)

@router.delete("/reviews/{review_id}")
async def delete_review(
    review_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Delete review (author or admin only)"""
    review_data = await db.reviews.find_one({"id": review_id})
    if not review_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    # Check ownership
    if (current_user.id != review_data["user_id"] and 
        current_user.role != UserRole.admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own reviews"
        )
    
    property_id = review_data["property_id"]
    
    # Delete review
    await db.reviews.delete_one({"id": review_id})
    
    # Update property rating
    await update_property_rating(db, property_id)
    
    return {"message": "Review deleted successfully"}

async def update_property_rating(db: AsyncIOMotorDatabase, property_id: str):
    """Update property's average rating and review count"""
    # Calculate new average rating
    pipeline = [
        {"$match": {"property_id": property_id}},
        {"$group": {
            "_id": None,
            "average_rating": {"$avg": "$rating"},
            "review_count": {"$sum": 1}
        }}
    ]
    
    result = await db.reviews.aggregate(pipeline).to_list(1)
    
    if result:
        avg_rating = round(result[0]["average_rating"], 1)
        review_count = result[0]["review_count"]
    else:
        avg_rating = None
        review_count = 0
    
    # Update property
    await db.properties.update_one(
        {"id": property_id},
        {"$set": {
            "average_rating": avg_rating,
            "review_count": review_count,
            "updated_at": datetime.utcnow()
        }}
    )