from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from datetime import datetime, date

from models import (
    Booking, BookingCreate, BookingUpdate, BookingResponse,
    User, BookingStatus, PaymentStatus, Property
)
from auth import get_current_active_user
from database import get_database

router = APIRouter(prefix="/api/bookings", tags=["bookings"])

async def check_property_availability(
    db: AsyncIOMotorDatabase,
    property_id: str,
    check_in: date,
    check_out: date,
    exclude_booking_id: str = None
) -> bool:
    """Check if property is available for given dates"""
    filter_query = {
        "property_id": property_id,
        "status": {"$in": ["confirmed", "pending"]},
        "$or": [
            {"check_in": {"$lte": check_out}, "check_out": {"$gte": check_in}}
        ]
    }
    
    if exclude_booking_id:
        filter_query["id"] = {"$ne": exclude_booking_id}
    
    conflicting_booking = await db.bookings.find_one(filter_query)
    return conflicting_booking is None

async def calculate_booking_price(
    db: AsyncIOMotorDatabase,
    property_id: str,
    check_in: date,
    check_out: date
) -> float:
    """Calculate total booking price"""
    property_data = await db.properties.find_one({"id": property_id})
    if not property_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    nights = (check_out - check_in).days
    if nights <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Check-out must be after check-in"
        )
    
    price_per_night = property_data["price_per_night"]
    
    # TODO: Apply seasonal pricing, special offers, etc.
    total_price = price_per_night * nights
    
    return total_price

@router.post("", response_model=BookingResponse)
async def create_booking(
    booking_data: BookingCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Create a new booking"""
    # Verify property exists and is active
    property_data = await db.properties.find_one({
        "id": booking_data.property_id,
        "is_active": True
    })
    if not property_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found or inactive"
        )
    
    # Check guest capacity
    if booking_data.guests > property_data["max_guests"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Property can accommodate maximum {property_data['max_guests']} guests"
        )
    
    # Check availability
    is_available = await check_property_availability(
        db, booking_data.property_id, booking_data.check_in, booking_data.check_out
    )
    if not is_available:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Property is not available for the selected dates"
        )
    
    # Calculate total price
    total_price = await calculate_booking_price(
        db, booking_data.property_id, booking_data.check_in, booking_data.check_out
    )
    
    # Create booking
    booking = Booking(
        **booking_data.dict(),
        user_id=current_user.id,
        total_price=total_price
    )
    
    await db.bookings.insert_one(booking.dict())
    
    # Return booking with property details
    property_obj = Property(**property_data)
    return BookingResponse(**booking.dict(), property=property_obj)

@router.get("", response_model=List[BookingResponse])
async def list_user_bookings(
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get current user's bookings"""
    bookings_data = await db.bookings.find({
        "user_id": current_user.id
    }).sort("created_at", -1).to_list(None)
    
    # Enrich with property data
    bookings = []
    for booking_data in bookings_data:
        booking = Booking(**booking_data)
        
        # Get property info
        property_data = await db.properties.find_one({"id": booking.property_id})
        property_obj = Property(**property_data) if property_data else None
        
        bookings.append(BookingResponse(**booking.dict(), property=property_obj))
    
    return bookings

@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(
    booking_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get single booking by ID"""
    booking_data = await db.bookings.find_one({"id": booking_id})
    if not booking_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Check ownership (users can only see their own bookings, unless admin/owner)
    if (current_user.id != booking_data["user_id"] and 
        current_user.role not in ["admin", "owner"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own bookings"
        )
    
    booking = Booking(**booking_data)
    
    # Get property info
    property_data = await db.properties.find_one({"id": booking.property_id})
    property_obj = Property(**property_data) if property_data else None
    
    return BookingResponse(**booking.dict(), property=property_obj)

@router.put("/{booking_id}", response_model=BookingResponse)
async def update_booking(
    booking_id: str,
    updates: BookingUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Update booking (only if not confirmed yet)"""
    booking_data = await db.bookings.find_one({"id": booking_id})
    if not booking_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Check ownership
    if current_user.id != booking_data["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own bookings"
        )
    
    # Check if booking can be modified
    if booking_data["status"] == BookingStatus.confirmed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot modify confirmed booking"
        )
    
    # Prepare update data
    update_data = {}
    for field, value in updates.dict(exclude_unset=True).items():
        if value is not None:
            update_data[field] = value
    
    # If dates are being updated, check availability and recalculate price
    if "check_in" in update_data or "check_out" in update_data:
        new_check_in = update_data.get("check_in", booking_data["check_in"])
        new_check_out = update_data.get("check_out", booking_data["check_out"])
        
        # Check availability (exclude current booking)
        is_available = await check_property_availability(
            db, booking_data["property_id"], new_check_in, new_check_out, booking_id
        )
        if not is_available:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Property is not available for the selected dates"
            )
        
        # Recalculate price
        new_total_price = await calculate_booking_price(
            db, booking_data["property_id"], new_check_in, new_check_out
        )
        update_data["total_price"] = new_total_price
    
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
        await db.bookings.update_one(
            {"id": booking_id},
            {"$set": update_data}
        )
    
    # Return updated booking
    updated_data = await db.bookings.find_one({"id": booking_id})
    booking = Booking(**updated_data)
    
    # Get property info
    property_data = await db.properties.find_one({"id": booking.property_id})
    property_obj = Property(**property_data) if property_data else None
    
    return BookingResponse(**booking.dict(), property=property_obj)

@router.delete("/{booking_id}")
async def cancel_booking(
    booking_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Cancel a booking"""
    booking_data = await db.bookings.find_one({"id": booking_id})
    if not booking_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Check ownership
    if current_user.id != booking_data["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only cancel your own bookings"
        )
    
    # Update booking status
    await db.bookings.update_one(
        {"id": booking_id},
        {"$set": {
            "status": BookingStatus.cancelled,
            "updated_at": datetime.utcnow()
        }}
    )
    
    return {"message": "Booking cancelled successfully"}

@router.post("/{booking_id}/payment")
async def process_payment(
    booking_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Process payment for booking (mock implementation)"""
    booking_data = await db.bookings.find_one({"id": booking_id})
    if not booking_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Check ownership
    if current_user.id != booking_data["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only pay for your own bookings"
        )
    
    # Mock payment processing
    # In real implementation, integrate with payment gateway (Stripe, PayPal, etc.)
    
    # Update booking status
    await db.bookings.update_one(
        {"id": booking_id},
        {"$set": {
            "status": BookingStatus.confirmed,
            "payment_status": PaymentStatus.completed,
            "updated_at": datetime.utcnow()
        }}
    )
    
    return {
        "message": "Payment processed successfully",
        "booking_id": booking_id,
        "status": "confirmed"
    }