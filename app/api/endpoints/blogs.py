"""
Blog API endpoints
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.base import get_db
from app.services.blog_service import BlogService
from app.schemas.blog import (
    BlogResponse, 
    BlogDetailResponse, 
    BlogCreate, 
    BlogUpdate
)
from app.schemas.asset import AssetAttachRequest

router = APIRouter()


@router.get("/", response_model=List[BlogResponse])
def get_blogs(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    project_id: int = Query(None, description="Filter by project ID"),
    db: Session = Depends(get_db)
):
    """Get all blogs with pagination and optional project filter"""
    if project_id:
        blogs = BlogService.get_blogs_by_project(db, project_id)
    else:
        blogs = BlogService.get_blogs(db, skip=skip, limit=limit)
    return blogs


@router.get("/{blog_id}", response_model=BlogDetailResponse)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    """Get blog by ID with related data"""
    blog = BlogService.get_blog_by_id(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@router.post("/", response_model=BlogResponse, status_code=201)
def create_blog(blog_data: BlogCreate, db: Session = Depends(get_db)):
    """Create new blog"""
    blog = BlogService.create_blog(db, blog_data)
    return blog


@router.patch("/{blog_id}", response_model=BlogResponse)
def update_blog(
    blog_id: int, 
    blog_data: BlogUpdate, 
    db: Session = Depends(get_db)
):
    """Update blog"""
    blog = BlogService.update_blog(db, blog_id, blog_data)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@router.delete("/{blog_id}")
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    """Delete blog"""
    success = BlogService.delete_blog(db, blog_id)
    if not success:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"message": "Blog deleted successfully"}


@router.post("/{blog_id}/assets/attach", response_model=BlogDetailResponse)
def attach_assets_to_blog(
    blog_id: int,
    request: AssetAttachRequest,
    db: Session = Depends(get_db)
):
    """Attach assets to blog"""
    blog = BlogService.attach_assets_to_blog(db, blog_id, request.asset_ids)
    return blog


@router.post("/{blog_id}/assets/detach", response_model=BlogDetailResponse)
def detach_assets_from_blog(
    blog_id: int,
    request: AssetAttachRequest,
    db: Session = Depends(get_db)
):
    """Detach assets from blog"""
    blog = BlogService.detach_assets_from_blog(db, blog_id, request.asset_ids)
    return blog
