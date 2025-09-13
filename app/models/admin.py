"""
Admin user and session models
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.base import Base


class AdminUser(Base):
    __tablename__ = "admin_users"

    admin_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    sessions = relationship("AdminSession", back_populates="admin_user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<AdminUser(id={self.admin_id}, username='{self.username}')>"


class AdminSession(Base):
    __tablename__ = "admin_sessions"

    session_id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("admin_users.admin_id", ondelete="CASCADE"), nullable=False)
    session_token = Column(String(255), nullable=False, unique=True, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    admin_user = relationship("AdminUser", back_populates="sessions")

    def __repr__(self):
        return f"<AdminSession(id={self.session_id}, admin_id={self.admin_id})>"
