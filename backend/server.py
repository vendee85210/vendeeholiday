from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path

# Import database and route modules
from database import connect_to_mongo, close_mongo_connection, init_sample_data, get_database
from routes.auth_routes import router as auth_router
from routes.property_routes import router as property_router
from routes.destination_routes import router as destination_router
from routes.booking_routes import router as booking_router
from routes.blog_routes import router as blog_router
from routes.content_routes import router as content_router
from routes.review_routes import router as review_router

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app
app = FastAPI(
    title="Pure France API",
    description="Holiday rental platform API",
    version="1.0.0"
)

# Global database reference for auth module
db = None

@app.on_event("startup")
async def startup_db_client():
    """Initialize database connection and sample data"""
    global db
    await connect_to_mongo()
    from database import db_instance
    db = db_instance.database
    await init_sample_data()
    print("Pure France API started successfully")

@app.on_event("shutdown")
async def shutdown_db_client():
    """Close database connection"""
    await close_mongo_connection()
    print("Database connection closed")

# Health check endpoint
@app.get("/api/")
async def root():
    return {"message": "Pure France API is running", "status": "healthy"}

# Include all routers
app.include_router(auth_router)
app.include_router(property_router)
app.include_router(destination_router)
app.include_router(booking_router)
app.include_router(blog_router)
app.include_router(content_router)
app.include_router(review_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
