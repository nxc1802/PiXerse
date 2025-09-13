"""
Member model
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.base import Base


class Member(Base):
    __tablename__ = "members"

    member_id = Column(Integer, primary_key=True, index=True)
    member_name = Column(String(255), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.project_id", ondelete="CASCADE"), nullable=True)  # nullable for general members
    team_type = Column(String(50), nullable=False)
    role = Column(String(50), nullable=False)
    experience = Column(Integer, nullable=False)
    summary = Column(Text, nullable=True)
    avatar_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    project = relationship("Project", back_populates="members")
    assets = relationship("Asset", secondary="member_assets", back_populates="members")
    blogs = relationship("Blog", back_populates="author")

    def __repr__(self):
        return f"<Member(id={self.member_id}, name='{self.member_name}', role='{self.role}', team_type='{self.team_type}')>"
