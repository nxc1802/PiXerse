"""
Blog model
"""

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.base import Base


class Blog(Base):
    __tablename__ = "blogs"

    blog_id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.project_id", ondelete="CASCADE"), nullable=False)
    title = Column(Text, nullable=False)
    detail = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    project = relationship("Project", back_populates="blogs")
    assets = relationship("Asset", secondary="blog_assets", back_populates="blogs")

    def __repr__(self):
        return f"<Blog(id={self.blog_id}, title='{self.title[:50]}...')>"
