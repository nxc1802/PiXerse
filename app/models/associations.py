"""
Association tables for many-to-many relationships
"""

from sqlalchemy import Table, Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.database.base import Base

# Project-Asset association table
project_assets = Table(
    'project_assets',
    Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.project_id', ondelete='CASCADE'), primary_key=True),
    Column('asset_id', Integer, ForeignKey('assets.asset_id', ondelete='CASCADE'), primary_key=True),
    Column('created_at', DateTime(timezone=True), server_default=func.now())
)

# Blog-Asset association table
blog_assets = Table(
    'blog_assets',
    Base.metadata,
    Column('blog_id', Integer, ForeignKey('blogs.blog_id', ondelete='CASCADE'), primary_key=True),
    Column('asset_id', Integer, ForeignKey('assets.asset_id', ondelete='CASCADE'), primary_key=True),
    Column('created_at', DateTime(timezone=True), server_default=func.now())
)

# Member-Asset association table
member_assets = Table(
    'member_assets',
    Base.metadata,
    Column('member_id', Integer, ForeignKey('members.member_id', ondelete='CASCADE'), primary_key=True),
    Column('asset_id', Integer, ForeignKey('assets.asset_id', ondelete='CASCADE'), primary_key=True),
    Column('created_at', DateTime(timezone=True), server_default=func.now())
)
