from fastapi import APIRouter, Depends, HTTPException, status, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional

from models import BlogPost, BlogPostResponse, User
from auth import get_current_active_user
from database import get_database

router = APIRouter(prefix="/api/blog", tags=["blog"])

@router.get("/posts", response_model=List[BlogPostResponse])
async def list_blog_posts(
    published: bool = Query(True, description="Filter by published status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get list of blog posts"""
    filter_query = {}
    if published:
        filter_query["published"] = True
    
    # Sort by published date (newest first)
    cursor = db.blog_posts.find(filter_query).sort("published_at", -1).skip(skip).limit(limit)
    posts_data = await cursor.to_list(limit)
    
    # Enrich with author data
    posts = []
    for post_data in posts_data:
        post = BlogPost(**post_data)
        
        # Get author info if available
        author = None
        if post.author_id:
            author_data = await db.users.find_one({"id": post.author_id})
            if author_data:
                from models import UserResponse
                author = UserResponse(
                    id=author_data["id"],
                    email=author_data["email"],
                    first_name=author_data["first_name"],
                    last_name=author_data["last_name"],
                    role=author_data["role"],
                    created_at=author_data["created_at"]
                )
        
        posts.append(BlogPostResponse(**post.dict(), author=author))
    
    return posts

@router.get("/posts/{slug}", response_model=BlogPostResponse)
async def get_blog_post(
    slug: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get single blog post by slug"""
    post_data = await db.blog_posts.find_one({"slug": slug, "published": True})
    if not post_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog post not found"
        )
    
    post = BlogPost(**post_data)
    
    # Get author info
    author = None
    if post.author_id:
        author_data = await db.users.find_one({"id": post.author_id})
        if author_data:
            from models import UserResponse
            author = UserResponse(
                id=author_data["id"],
                email=author_data["email"],
                first_name=author_data["first_name"],
                last_name=author_data["last_name"],
                role=author_data["role"],
                created_at=author_data["created_at"]
            )
    
    return BlogPostResponse(**post.dict(), author=author)