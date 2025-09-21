from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
import os
from datetime import datetime

class Database:
    client: Optional[AsyncIOMotorClient] = None
    database: Optional[AsyncIOMotorDatabase] = None

db_instance = Database()

async def connect_to_mongo():
    """Create database connection"""
    mongo_url = os.environ.get("MONGO_URL")
    db_name = os.environ.get("DB_NAME", "purefrance")
    
    db_instance.client = AsyncIOMotorClient(mongo_url)
    db_instance.database = db_instance.client[db_name]
    
    # Create indexes for better performance
    await create_indexes()
    
    print(f"Connected to MongoDB: {db_name}")

async def close_mongo_connection():
    """Close database connection"""
    if db_instance.client:
        db_instance.client.close()

async def get_database() -> AsyncIOMotorDatabase:
    """Get database instance"""
    return db_instance.database

async def create_indexes():
    """Create database indexes for better performance"""
    db = db_instance.database
    
    # User indexes
    await db.users.create_index("email", unique=True)
    await db.users.create_index("id", unique=True)
    
    # Property indexes
    await db.properties.create_index("id", unique=True)
    await db.properties.create_index("owner_id")
    await db.properties.create_index("location.region")
    await db.properties.create_index("property_type")
    await db.properties.create_index("price_per_night")
    await db.properties.create_index("is_active")
    await db.properties.create_index([("location.latitude", 1), ("location.longitude", 1)])
    
    # Booking indexes
    await db.bookings.create_index("id", unique=True)
    await db.bookings.create_index("user_id")
    await db.bookings.create_index("property_id")
    await db.bookings.create_index([("check_in", 1), ("check_out", 1)])
    await db.bookings.create_index("status")
    
    # Blog post indexes
    await db.blog_posts.create_index("slug", unique=True)
    await db.blog_posts.create_index("published")
    await db.blog_posts.create_index("published_at")
    
    # Review indexes
    await db.reviews.create_index("property_id")
    await db.reviews.create_index("user_id")
    await db.reviews.create_index("rating")
    
    # Session indexes
    await db.sessions.create_index("token", unique=True)
    await db.sessions.create_index("user_id")
    await db.sessions.create_index("expires_at", expireAfterSeconds=0)
    
    # Destination indexes
    await db.destinations.create_index("slug", unique=True)
    await db.destinations.create_index("featured")
    
    # Special offer indexes
    await db.special_offers.create_index("active")
    await db.special_offers.create_index([("valid_from", 1), ("valid_until", 1)])

async def init_sample_data():
    """Initialize database with sample data"""
    db = db_instance.database
    
    # Check if data already exists
    destination_count = await db.destinations.count_documents({})
    if destination_count > 0:
        return  # Data already exists
    
    # Create sample destinations
    destinations_data = [
        {
            "id": "dest-1",
            "name": "Loire, Vendée, Brittany and Burgundy",
            "slug": "loire-vendee-brittany-burgundy",
            "description": "The beautiful heart of Central France",
            "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=600&fit=crop",
            "region_type": "Central France",
            "featured": True,
            "property_count": 0,
            "created_at": datetime.utcnow()
        },
        {
            "id": "dest-2", 
            "name": "Dordogne and South-West",
            "slug": "dordogne-south-west",
            "description": "The much-loved South-West",
            "image_url": "https://images.unsplash.com/photo-1516548043878-4e9a92085ba8?w=800&h=600&fit=crop",
            "region_type": "South-West France",
            "featured": True,
            "property_count": 0,
            "created_at": datetime.utcnow()
        },
        {
            "id": "dest-3",
            "name": "Occitanie (inc. Languedoc)",
            "slug": "languedoc-occitanie", 
            "description": "The sun-drenched Mediterranean",
            "image_url": "https://images.unsplash.com/photo-1549144511-f099e773c147?w=800&h=600&fit=crop",
            "region_type": "Mediterranean",
            "featured": True,
            "property_count": 0,
            "created_at": datetime.utcnow()
        },
        {
            "id": "dest-4",
            "name": "Provence, Côte d'Azur and Corsica",
            "slug": "provence-cote-d-azur-corsica",
            "description": "Picturesque villages and the French Riviera",
            "image_url": "https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=800&h=600&fit=crop",
            "region_type": "South France",
            "featured": True,
            "property_count": 0,
            "created_at": datetime.utcnow()
        }
    ]
    
    await db.destinations.insert_many(destinations_data)
    
    # Create sample inspiration categories
    inspiration_data = [
        {
            "id": "insp-1",
            "title": "Perfect for couples",
            "slug": "couples",
            "description": "Romantic getaways in beautiful French settings",
            "image_url": "https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=800&h=600&fit=crop",
            "property_count": 0,
            "created_at": datetime.utcnow()
        },
        {
            "id": "insp-2",
            "title": "Large groups 12+",
            "slug": "large-groups",
            "description": "Spacious properties for family reunions and group holidays",
            "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&h=600&fit=crop",
            "property_count": 0,
            "created_at": datetime.utcnow()
        },
        {
            "id": "insp-3",
            "title": "Short stays",
            "slug": "short-breaks",
            "description": "Perfect for weekend getaways and short breaks",
            "image_url": "https://images.unsplash.com/photo-1502672023488-70e25813eb80?w=800&h=600&fit=crop",
            "property_count": 0,
            "created_at": datetime.utcnow()
        },
        {
            "id": "insp-4",
            "title": "Pets considered",
            "slug": "pet-friendly",
            "description": "Pet-friendly properties for holidays with your furry friends",
            "image_url": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=800&h=600&fit=crop",
            "property_count": 0,
            "created_at": datetime.utcnow()
        }
    ]
    
    await db.inspiration_categories.insert_many(inspiration_data)
    
    # Create sample blog posts
    blog_data = [
        {
            "id": "blog-1",
            "title": "The lovely town of Pornic on France's Cote de Jade",
            "slug": "pornic-cote-de-jade",
            "excerpt": "Discover the charming coastal town of Pornic and its beautiful surroundings on the Jade Coast.",
            "content": "Pornic is a beautiful coastal town located on France's Jade Coast...",
            "featured_image": "https://images.unsplash.com/photo-1549144511-f099e773c147?w=800&h=600&fit=crop",
            "author_id": "admin-1",
            "published": True,
            "published_at": datetime.utcnow(),
            "created_at": datetime.utcnow()
        },
        {
            "id": "blog-2",
            "title": "Unusual historical places to visit in France",
            "slug": "unusual-historical-places",
            "excerpt": "Explore France's hidden historical gems beyond the typical tourist attractions.",
            "content": "France is filled with fascinating historical sites...",
            "featured_image": "https://images.unsplash.com/photo-1558618047-b2b89c4a2868?w=800&h=600&fit=crop",
            "author_id": "admin-1", 
            "published": True,
            "published_at": datetime.utcnow(),
            "created_at": datetime.utcnow()
        }
    ]
    
    await db.blog_posts.insert_many(blog_data)
    
    print("Sample data initialized successfully")