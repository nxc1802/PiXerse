"""
Asset CRUD service
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException

from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetUpdate
from app.services.cloudinary_service import CloudinaryService


class AssetService:
    @staticmethod
    def get_assets(db: Session, skip: int = 0, limit: int = 100) -> List[Asset]:
        """Get all assets with pagination"""
        return db.query(Asset).offset(skip).limit(limit).all()

    @staticmethod
    def get_asset_by_id(db: Session, asset_id: int) -> Optional[Asset]:
        """Get asset by ID"""
        return db.query(Asset).filter(Asset.asset_id == asset_id).first()

    @staticmethod
    def get_asset_by_public_id(db: Session, public_id: str) -> Optional[Asset]:
        """Get asset by Cloudinary public ID"""
        return db.query(Asset).filter(Asset.cloudinary_public_id == public_id).first()

    @staticmethod
    async def upload_and_create_asset(db: Session, file: UploadFile) -> Asset:
        """Upload file to Cloudinary and create asset record"""
        try:
            # Upload to Cloudinary
            upload_data = await CloudinaryService.upload_file(file)
            
            # Create asset record in database
            db_asset = Asset(**upload_data)
            db.add(db_asset)
            db.commit()
            db.refresh(db_asset)
            
            return db_asset
            
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to create asset: {str(e)}")

    @staticmethod
    def create_asset(db: Session, asset_data: AssetCreate) -> Asset:
        """Create asset record (for assets already uploaded to Cloudinary)"""
        # Check if asset with same public_id already exists
        existing_asset = AssetService.get_asset_by_public_id(db, asset_data.cloudinary_public_id)
        if existing_asset:
            raise HTTPException(status_code=400, detail="Asset with this public ID already exists")
        
        db_asset = Asset(
            filename=asset_data.filename,
            original_filename=asset_data.original_filename,
            cloudinary_public_id=asset_data.cloudinary_public_id,
            cloudinary_url=asset_data.cloudinary_url,
            cloudinary_secure_url=asset_data.cloudinary_secure_url,
            asset_type=asset_data.asset_type,
            file_size=asset_data.file_size,
            mime_type=asset_data.mime_type,
            width=asset_data.width,
            height=asset_data.height
        )
        db.add(db_asset)
        db.commit()
        db.refresh(db_asset)
        return db_asset

    @staticmethod
    def update_asset(db: Session, asset_id: int, asset_data: AssetUpdate) -> Optional[Asset]:
        """Update asset metadata"""
        db_asset = AssetService.get_asset_by_id(db, asset_id)
        if not db_asset:
            return None
        
        # Update only provided fields
        update_data = asset_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_asset, field, value)
        
        db.commit()
        db.refresh(db_asset)
        return db_asset

    @staticmethod
    def delete_asset(db: Session, asset_id: int, delete_from_cloudinary: bool = True) -> bool:
        """Delete asset and optionally remove from Cloudinary"""
        db_asset = AssetService.get_asset_by_id(db, asset_id)
        if not db_asset:
            return False
        
        # Delete from Cloudinary if requested
        if delete_from_cloudinary:
            cloudinary_deleted = CloudinaryService.delete_file(db_asset.cloudinary_public_id)
            if not cloudinary_deleted:
                # Log warning but continue with database deletion
                print(f"Warning: Failed to delete asset {db_asset.cloudinary_public_id} from Cloudinary")
        
        # Delete from database
        db.delete(db_asset)
        db.commit()
        return True

    @staticmethod
    def get_assets_by_type(db: Session, asset_type: str, skip: int = 0, limit: int = 100) -> List[Asset]:
        """Get assets filtered by type"""
        return db.query(Asset).filter(Asset.asset_type == asset_type).offset(skip).limit(limit).all()

    @staticmethod
    def search_assets(db: Session, search_term: str, skip: int = 0, limit: int = 100) -> List[Asset]:
        """Search assets by filename or original filename"""
        search_pattern = f"%{search_term}%"
        return db.query(Asset).filter(
            (Asset.filename.ilike(search_pattern)) | 
            (Asset.original_filename.ilike(search_pattern))
        ).offset(skip).limit(limit).all()
