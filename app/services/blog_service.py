"""
Blog CRUD service
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.blog import Blog
from app.models.asset import Asset
from app.schemas.blog import BlogCreate, BlogUpdate
from app.services.project_service import ProjectService


class BlogService:
    @staticmethod
    def get_blogs(db: Session, skip: int = 0, limit: int = 100) -> List[Blog]:
        """Get all blogs with pagination"""
        return db.query(Blog).offset(skip).limit(limit).all()

    @staticmethod
    def get_blog_by_id(db: Session, blog_id: int) -> Optional[Blog]:
        """Get blog by ID"""
        return db.query(Blog).filter(Blog.blog_id == blog_id).first()

    @staticmethod
    def get_blogs_by_project(db: Session, project_id: int) -> List[Blog]:
        """Get all blogs of a specific project"""
        return db.query(Blog).filter(Blog.project_id == project_id).all()

    @staticmethod
    def create_blog(db: Session, blog_data: BlogCreate) -> Blog:
        """Create new blog"""
        # Verify project exists
        project = ProjectService.get_project_by_id(db, blog_data.project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        db_blog = Blog(
            project_id=blog_data.project_id,
            title=blog_data.title,
            detail=blog_data.detail
        )
        db.add(db_blog)
        db.commit()
        db.refresh(db_blog)
        return db_blog

    @staticmethod
    def update_blog(db: Session, blog_id: int, blog_data: BlogUpdate) -> Optional[Blog]:
        """Update blog"""
        db_blog = BlogService.get_blog_by_id(db, blog_id)
        if not db_blog:
            return None
        
        # Update only provided fields
        update_data = blog_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_blog, field, value)
        
        db.commit()
        db.refresh(db_blog)
        return db_blog

    @staticmethod
    def delete_blog(db: Session, blog_id: int) -> bool:
        """Delete blog"""
        db_blog = BlogService.get_blog_by_id(db, blog_id)
        if not db_blog:
            return False
        
        db.delete(db_blog)
        db.commit()
        return True

    @staticmethod
    def attach_assets_to_blog(db: Session, blog_id: int, asset_ids: List[int]) -> Optional[Blog]:
        """Attach assets to blog"""
        db_blog = BlogService.get_blog_by_id(db, blog_id)
        if not db_blog:
            raise HTTPException(status_code=404, detail="Blog not found")
        
        # Get assets
        assets = db.query(Asset).filter(Asset.asset_id.in_(asset_ids)).all()
        if len(assets) != len(asset_ids):
            found_ids = [asset.asset_id for asset in assets]
            missing_ids = [aid for aid in asset_ids if aid not in found_ids]
            raise HTTPException(status_code=404, detail=f"Assets not found: {missing_ids}")
        
        # Attach assets (avoid duplicates)
        for asset in assets:
            if asset not in db_blog.assets:
                db_blog.assets.append(asset)
        
        db.commit()
        db.refresh(db_blog)
        return db_blog

    @staticmethod
    def detach_assets_from_blog(db: Session, blog_id: int, asset_ids: List[int]) -> Optional[Blog]:
        """Detach assets from blog"""
        db_blog = BlogService.get_blog_by_id(db, blog_id)
        if not db_blog:
            raise HTTPException(status_code=404, detail="Blog not found")
        
        # Remove assets
        for asset_id in asset_ids:
            asset_to_remove = next((asset for asset in db_blog.assets if asset.asset_id == asset_id), None)
            if asset_to_remove:
                db_blog.assets.remove(asset_to_remove)
        
        db.commit()
        db.refresh(db_blog)
        return db_blog
