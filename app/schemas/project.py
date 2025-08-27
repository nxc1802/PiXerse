"""
Project schemas for request/response
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class ProjectBase(BaseModel):
    project_name: str = Field(..., min_length=1, max_length=255, description="Project name")
    description: Optional[str] = Field(None, description="Project description")


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    project_name: Optional[str] = Field(None, min_length=1, max_length=255, description="Project name")
    description: Optional[str] = Field(None, description="Project description")


class ProjectResponse(ProjectBase):
    project_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class ProjectDetailResponse(ProjectResponse):
    # Include related data
    members: List["MemberResponse"] = []
    blogs: List["BlogResponse"] = []
    assets: List["AssetResponse"] = []

    model_config = ConfigDict(from_attributes=True)


# Forward references for circular imports
from app.schemas.member import MemberResponse  # noqa: E402
from app.schemas.blog import BlogResponse  # noqa: E402  
from app.schemas.asset import AssetResponse  # noqa: E402

ProjectDetailResponse.model_rebuild()
