"""
Asset model for managing Cloudinary files and YouTube embeds
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.database.base import Base


class AssetType(enum.Enum):
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    YOUTUBE = "YOUTUBE"


class Asset(Base):
    __tablename__ = "assets"

    asset_id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=True)  # nullable for YouTube
    cloudinary_public_id = Column(String(255), nullable=True, unique=True, index=True)  # nullable for YouTube
    cloudinary_url = Column(Text, nullable=True)  # nullable for YouTube
    asset_type = Column(Enum(AssetType), nullable=False, default=AssetType.IMAGE)
    file_size = Column(BigInteger, nullable=True, default=0)  # 0 for YouTube
    mime_type = Column(String(100), nullable=True)  # nullable for YouTube
    width = Column(Integer, nullable=True)  # For images/videos
    height = Column(Integer, nullable=True)  # For images/videos
    youtube_video_id = Column(String(100), nullable=True)  # for YouTube videos
    description = Column(Text, nullable=True)  # alt text or video description
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships with association tables
    projects = relationship("Project", secondary="project_assets", back_populates="assets")
    blogs = relationship("Blog", secondary="blog_assets", back_populates="assets")
    members = relationship("Member", secondary="member_assets", back_populates="assets")

    def __repr__(self):
        return f"<Asset(id={self.asset_id}, filename='{self.filename}', type='{self.asset_type.value}')>"
