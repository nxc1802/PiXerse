"""
Asset schemas for request/response
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.models.asset import AssetType


class AssetBase(BaseModel):
    filename: str = Field(..., description="Asset filename")
    original_filename: Optional[str] = Field(None, description="Original filename when uploaded (nullable for YouTube)")
    cloudinary_public_id: Optional[str] = Field(None, description="Cloudinary public ID (nullable for YouTube)")
    cloudinary_url: Optional[str] = Field(None, description="Cloudinary URL (nullable for YouTube)")
    asset_type: AssetType = Field(default=AssetType.IMAGE, description="Asset type")
    file_size: Optional[int] = Field(0, description="File size in bytes (0 for YouTube)")
    mime_type: Optional[str] = Field(None, description="MIME type (nullable for YouTube)")
    width: Optional[int] = Field(None, description="Width for images/videos")
    height: Optional[int] = Field(None, description="Height for images/videos")
    youtube_video_id: Optional[str] = Field(None, max_length=100, description="YouTube video ID")
    description: Optional[str] = Field(None, description="Alt text or video description")


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    filename: Optional[str] = Field(None, description="Asset filename")
    asset_type: Optional[AssetType] = Field(None, description="Asset type")
    youtube_video_id: Optional[str] = Field(None, max_length=100, description="YouTube video ID")
    description: Optional[str] = Field(None, description="Alt text or video description")


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


# YouTube embed schema
class YouTubeEmbedRequest(BaseModel):
    youtube_video_id: str = Field(..., min_length=1, max_length=100, description="YouTube video ID")
    description: Optional[str] = Field(None, description="Video description")
    
    
class AssetAttachRequest(BaseModel):
    asset_ids: List[int] = Field(..., description="List of asset IDs to attach")


# Forward references for circular imports
from app.schemas.project import ProjectResponse  # noqa: E402
from app.schemas.blog import BlogResponse  # noqa: E402
from app.schemas.member import MemberResponse  # noqa: E402

AssetDetailResponse.model_rebuild()
