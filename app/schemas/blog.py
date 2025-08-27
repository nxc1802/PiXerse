"""
Blog schemas for request/response
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class BlogBase(BaseModel):
    project_id: int = Field(..., description="Project ID this blog belongs to")
    title: str = Field(..., min_length=1, description="Blog title")
    detail: Optional[str] = Field(None, description="Blog content detail")


class BlogCreate(BlogBase):
    pass


class BlogUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, description="Blog title")
    detail: Optional[str] = Field(None, description="Blog content detail")


class BlogResponse(BlogBase):
    blog_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class BlogDetailResponse(BlogResponse):
    # Include related data
    project: Optional["ProjectResponse"] = None
    assets: List["AssetResponse"] = []

    model_config = ConfigDict(from_attributes=True)


# Forward references for circular imports
from app.schemas.project import ProjectResponse  # noqa: E402
from app.schemas.asset import AssetResponse  # noqa: E402

BlogDetailResponse.model_rebuild()
