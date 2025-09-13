"""
Blog schemas for request/response
"""

from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, Field, ConfigDict


class BlogBase(BaseModel):
    project_id: Optional[int] = Field(None, description="Project ID this blog belongs to (nullable for general blogs)")
    author_id: int = Field(..., description="Author member ID")
    title: str = Field(..., min_length=1, max_length=500, description="Blog title")
    content: str = Field(..., description="Blog content")
    category: Optional[str] = Field(None, max_length=50, description="Blog category (tutorial, news, showcase)")
    tags: Optional[List[str]] = Field(None, description="Array of tags")
    featured_image: Optional[str] = Field(None, max_length=500, description="Featured image URL")


class BlogCreate(BlogBase):
    pass


class BlogUpdate(BaseModel):
    project_id: Optional[int] = Field(None, description="Project ID this blog belongs to")
    author_id: Optional[int] = Field(None, description="Author member ID")
    title: Optional[str] = Field(None, min_length=1, max_length=500, description="Blog title")
    content: Optional[str] = Field(None, description="Blog content")
    category: Optional[str] = Field(None, max_length=50, description="Blog category")
    tags: Optional[List[str]] = Field(None, description="Array of tags")
    featured_image: Optional[str] = Field(None, max_length=500, description="Featured image URL")


class BlogResponse(BlogBase):
    blog_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class BlogDetailResponse(BlogResponse):
    # Include related data
    project: Optional["ProjectResponse"] = None
    author: Optional["MemberResponse"] = None
    assets: List["AssetResponse"] = []

    model_config = ConfigDict(from_attributes=True)


# Forward references for circular imports
from app.schemas.project import ProjectResponse  # noqa: E402
from app.schemas.asset import AssetResponse  # noqa: E402
from app.schemas.member import MemberResponse  # noqa: E402

BlogDetailResponse.model_rebuild()
