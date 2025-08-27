"""
Asset schemas for request/response
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.models.asset import AssetType


class AssetBase(BaseModel):
    filename: str = Field(..., description="Asset filename")
    original_filename: str = Field(..., description="Original filename when uploaded")
    cloudinary_public_id: str = Field(..., description="Cloudinary public ID")
    cloudinary_url: str = Field(..., description="Cloudinary URL")
    cloudinary_secure_url: str = Field(..., description="Cloudinary secure URL")
    asset_type: AssetType = Field(default=AssetType.IMAGE, description="Asset type")
    file_size: Optional[int] = Field(None, description="File size in bytes")
    mime_type: Optional[str] = Field(None, description="MIME type")
    width: Optional[int] = Field(None, description="Width for images/videos")
    height: Optional[int] = Field(None, description="Height for images/videos")


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    filename: Optional[str] = Field(None, description="Asset filename")
    asset_type: Optional[AssetType] = Field(None, description="Asset type")


class AssetResponse(AssetBase):
    asset_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class AssetDetailResponse(AssetResponse):
    # Include related data
    projects: List["ProjectResponse"] = []
    blogs: List["BlogResponse"] = []
    members: List["MemberResponse"] = []

    model_config = ConfigDict(from_attributes=True)


# File upload schema
class FileUploadResponse(BaseModel):
    message: str
    asset: AssetResponse
    
    
class AssetAttachRequest(BaseModel):
    asset_ids: List[int] = Field(..., description="List of asset IDs to attach")


# Forward references for circular imports
from app.schemas.project import ProjectResponse  # noqa: E402
from app.schemas.blog import BlogResponse  # noqa: E402
from app.schemas.member import MemberResponse  # noqa: E402

AssetDetailResponse.model_rebuild()
