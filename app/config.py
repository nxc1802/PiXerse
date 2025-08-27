"""
Configuration settings for PiXerse Backend
"""

import os
from typing import List, Optional
from pydantic import field_validator, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application Configuration
    APP_NAME: str = "PiXerse Backend"
    DEBUG: bool = True
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB in bytes
    
    # Database Configuration
    DATABASE_URL: str
    
    # Cloudinary Configuration
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    CLOUDINARY_URL: Optional[str] = None
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080", "http://127.0.0.1:3000"]
    
    # Security Configuration
    SECRET_KEY: Optional[str] = None
    JWT_SECRET_KEY: Optional[str] = None
    
    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        if not v or not v.startswith("postgresql://"):
            raise ValueError("DATABASE_URL must be a valid PostgreSQL connection string")
        return v
    
    @field_validator("CLOUDINARY_CLOUD_NAME", mode="before")
    @classmethod
    def validate_cloudinary_cloud_name(cls, v: str) -> str:
        if not v:
            raise ValueError("CLOUDINARY_CLOUD_NAME is required")
        return v
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        env_file_encoding='utf-8'
    )


# Create settings instance
settings = Settings()
