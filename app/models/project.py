"""
Project model
"""

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.base import Base


class Project(Base):
    __tablename__ = "projects"

    project_id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    members = relationship("Member", back_populates="project", cascade="all, delete-orphan")
    blogs = relationship("Blog", back_populates="project", cascade="all, delete-orphan")
    assets = relationship("Asset", secondary="project_assets", back_populates="projects")

    def __repr__(self):
        return f"<Project(id={self.project_id}, name='{self.project_name}')>"
