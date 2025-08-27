"""
Member schemas for request/response
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class MemberBase(BaseModel):
    project_id: int = Field(..., description="Project ID this member belongs to")
    team_type: str = Field(..., min_length=1, max_length=50, description="Team type")
    role: str = Field(..., min_length=1, max_length=50, description="Member role")
    experience: int = Field(..., ge=0, description="Years of experience")
    summary: Optional[str] = Field(None, description="Member summary")


class MemberCreate(MemberBase):
    pass


class MemberUpdate(BaseModel):
    team_type: Optional[str] = Field(None, min_length=1, max_length=50, description="Team type")
    role: Optional[str] = Field(None, min_length=1, max_length=50, description="Member role")
    experience: Optional[int] = Field(None, ge=0, description="Years of experience")
    summary: Optional[str] = Field(None, description="Member summary")


class MemberResponse(MemberBase):
    member_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class MemberDetailResponse(MemberResponse):
    # Include related data
    project: Optional["ProjectResponse"] = None
    assets: List["AssetResponse"] = []

    model_config = ConfigDict(from_attributes=True)


# Forward references for circular imports
from app.schemas.project import ProjectResponse  # noqa: E402
from app.schemas.asset import AssetResponse  # noqa: E402

MemberDetailResponse.model_rebuild()
