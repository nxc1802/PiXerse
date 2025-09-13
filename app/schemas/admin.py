"""
Admin user and session schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class AdminUserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Admin username")
    full_name: str = Field(..., min_length=1, max_length=255, description="Full name")


class AdminUserCreate(AdminUserBase):
    password: str = Field(..., min_length=6, description="Admin password")


class AdminUserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="Admin username")
    full_name: Optional[str] = Field(None, min_length=1, max_length=255, description="Full name")
    password: Optional[str] = Field(None, min_length=6, description="Admin password")


class AdminUserResponse(AdminUserBase):
    admin_id: int
    created_at: datetime
    last_login_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class AdminUserLogin(BaseModel):
    username: str = Field(..., description="Admin username")
    password: str = Field(..., description="Admin password")


class AdminSessionResponse(BaseModel):
    session_id: int
    admin_id: int
    session_token: str
    expires_at: datetime
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class AdminLoginResponse(BaseModel):
    message: str
    admin: AdminUserResponse
    session: AdminSessionResponse
