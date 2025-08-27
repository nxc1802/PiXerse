"""
Asset API endpoints
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session

from app.database.base import get_db
from app.services.asset_service import AssetService
from app.schemas.asset import (
    AssetResponse, 
    AssetDetailResponse, 
    AssetCreate, 
    AssetUpdate,
    FileUploadResponse
)

router = APIRouter()


@router.get("/", response_model=List[AssetResponse])
def get_assets(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    asset_type: str = Query(None, description="Filter by asset type"),
    search: str = Query(None, description="Search by filename"),
    db: Session = Depends(get_db)
):
    """Get all assets with pagination and optional filters"""
    if search:
        assets = AssetService.search_assets(db, search, skip=skip, limit=limit)
    elif asset_type:
        assets = AssetService.get_assets_by_type(db, asset_type, skip=skip, limit=limit)
    else:
        assets = AssetService.get_assets(db, skip=skip, limit=limit)
    return assets


@router.get("/{asset_id}", response_model=AssetDetailResponse)
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    """Get asset by ID with related data"""
    asset = AssetService.get_asset_by_id(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.post("/upload", response_model=FileUploadResponse, status_code=201)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload file to Cloudinary and create asset record"""
    asset = await AssetService.upload_and_create_asset(db, file)
    return FileUploadResponse(
        message="File uploaded successfully",
        asset=asset
    )


@router.post("/", response_model=AssetResponse, status_code=201)
def create_asset(asset_data: AssetCreate, db: Session = Depends(get_db)):
    """Create asset record for already uploaded file"""
    asset = AssetService.create_asset(db, asset_data)
    return asset


@router.patch("/{asset_id}", response_model=AssetResponse)
def update_asset(
    asset_id: int, 
    asset_data: AssetUpdate, 
    db: Session = Depends(get_db)
):
    """Update asset metadata"""
    asset = AssetService.update_asset(db, asset_id, asset_data)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.delete("/{asset_id}")
def delete_asset(
    asset_id: int, 
    delete_from_cloudinary: bool = Query(True, description="Also delete from Cloudinary"),
    db: Session = Depends(get_db)
):
    """Delete asset and optionally remove from Cloudinary"""
    success = AssetService.delete_asset(db, asset_id, delete_from_cloudinary)
    if not success:
        raise HTTPException(status_code=404, detail="Asset not found")
    return {"message": "Asset deleted successfully"}
