from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from enum import Enum
import uuid

# Enums
class UserRole(str, Enum):
    guest = "guest"
    owner = "owner" 
    admin = "admin"

class BookingStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"

class PaymentStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"
    refunded = "refunded"

class PropertyType(str, Enum):
    villa = "villa"
    chateau = "chateau"
    cottage = "cottage"
    apartment = "apartment"
    farmhouse = "farmhouse"

# Base Models
class BaseDBModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

# User Models
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None

class User(UserBase, BaseDBModel):
    password_hash: str
    role: UserRole = UserRole.guest
    is_active: bool = True

class UserResponse(UserBase):
    id: str
    role: UserRole
    created_at: datetime

# Authentication Models
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class Session(BaseDBModel):
    user_id: str
    token: str
    expires_at: datetime

# Property Models
class PropertyImage(BaseModel):
    url: str
    alt_text: Optional[str] = None
    is_primary: bool = False

class Amenity(BaseModel):
    id: str
    name: str
    icon: Optional[str] = None
    category: Optional[str] = None

class Availability(BaseModel):
    start_date: date
    end_date: date
    price_per_night: float
    minimum_stay: int = 1

class PropertyLocation(BaseModel):
    address: str
    city: str
    region: str
    postal_code: str
    country: str = "France"
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class PropertyBase(BaseModel):
    name: str
    description: str
    bedrooms: int
    bathrooms: int
    max_guests: int
    property_type: PropertyType
    location: PropertyLocation
    price_per_night: float
    images: List[PropertyImage] = []
    amenities: List[str] = []  # Amenity IDs
    
    @validator('bedrooms', 'bathrooms', 'max_guests')
    def validate_positive(cls, v):
        if v <= 0:
            raise ValueError('Must be positive')
        return v

class PropertyCreate(PropertyBase):
    pass

class PropertyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    max_guests: Optional[int] = None
    price_per_night: Optional[float] = None
    images: Optional[List[PropertyImage]] = None
    amenities: Optional[List[str]] = None

class Property(PropertyBase, BaseDBModel):
    owner_id: str
    is_active: bool = True
    average_rating: Optional[float] = None
    review_count: int = 0

class PropertyResponse(Property):
    availability: List[Availability] = []
    owner: Optional[UserResponse] = None

# Destination Models
class DestinationBase(BaseModel):
    name: str
    slug: str
    description: str
    image_url: str
    region_type: str

class DestinationCreate(DestinationBase):
    pass

class Destination(DestinationBase, BaseDBModel):
    featured: bool = False
    property_count: int = 0

# Booking Models
class BookingBase(BaseModel):
    property_id: str
    check_in: date
    check_out: date
    guests: int
    special_requests: Optional[str] = None

    @validator('check_out')
    def validate_dates(cls, v, values):
        if 'check_in' in values and v <= values['check_in']:
            raise ValueError('Check-out must be after check-in')
        return v

    @validator('guests')
    def validate_guests(cls, v):
        if v <= 0:
            raise ValueError('Must have at least 1 guest')
        return v

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    check_in: Optional[date] = None
    check_out: Optional[date] = None
    guests: Optional[int] = None
    special_requests: Optional[str] = None

class Booking(BookingBase, BaseDBModel):
    user_id: str
    total_price: float
    status: BookingStatus = BookingStatus.pending
    payment_status: PaymentStatus = PaymentStatus.pending

class BookingResponse(Booking):
    property: Optional[Property] = None
    user: Optional[UserResponse] = None

# Blog Models
class BlogPostBase(BaseModel):
    title: str
    slug: str
    excerpt: Optional[str] = None
    content: str
    featured_image: Optional[str] = None

class BlogPostCreate(BlogPostBase):
    pass

class BlogPost(BlogPostBase, BaseDBModel):
    author_id: str
    published: bool = False
    published_at: Optional[datetime] = None

class BlogPostResponse(BlogPost):
    author: Optional[UserResponse] = None

# Inspiration Models
class InspirationCategoryBase(BaseModel):
    title: str
    slug: str
    description: Optional[str] = None
    image_url: str

class InspirationCategory(InspirationCategoryBase, BaseDBModel):
    property_count: int = 0

# Special Offer Models
class SpecialOfferBase(BaseModel):
    title: str
    description: str
    discount_percentage: float
    valid_from: datetime
    valid_until: datetime
    property_ids: List[str] = []

    @validator('discount_percentage')
    def validate_discount(cls, v):
        if v <= 0 or v > 100:
            raise ValueError('Discount must be between 0 and 100')
        return v

class SpecialOfferCreate(SpecialOfferBase):
    pass

class SpecialOffer(SpecialOfferBase, BaseDBModel):
    active: bool = True

# Review Models
class ReviewBase(BaseModel):
    rating: int
    title: str
    content: str

    @validator('rating')
    def validate_rating(cls, v):
        if v < 1 or v > 5:
            raise ValueError('Rating must be between 1 and 5')
        return v

class ReviewCreate(ReviewBase):
    property_id: str

class Review(ReviewBase, BaseDBModel):
    user_id: str
    property_id: str
    booking_id: Optional[str] = None

class ReviewResponse(Review):
    user: Optional[UserResponse] = None
    property: Optional[Property] = None

# Search Models
class PropertySearchFilters(BaseModel):
    region: Optional[str] = None
    check_in: Optional[date] = None
    check_out: Optional[date] = None
    guests: Optional[int] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    property_type: Optional[PropertyType] = None
    amenities: Optional[List[str]] = None
    bedrooms: Optional[int] = None

class SearchResponse(BaseModel):
    properties: List[Property]
    total_count: int
    filters_applied: PropertySearchFilters