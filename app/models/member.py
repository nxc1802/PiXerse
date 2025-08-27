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
    project_id = Column(Integer, ForeignKey("projects.project_id", ondelete="CASCADE"), nullable=False)
    team_type = Column(String(50), nullable=False)
    role = Column(String(50), nullable=False)
    experience = Column(Integer, nullable=False)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    project = relationship("Project", back_populates="members")
    assets = relationship("Asset", secondary="member_assets", back_populates="members")

    def __repr__(self):
        return f"<Member(id={self.member_id}, role='{self.role}', team_type='{self.team_type}')>"
