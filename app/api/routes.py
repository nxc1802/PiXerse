"""
Main API router that includes all endpoint routers
"""

from fastapi import APIRouter

from app.api.endpoints import projects, members, blogs, assets

# Create main API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(members.router, prefix="/members", tags=["members"])
api_router.include_router(blogs.router, prefix="/blogs", tags=["blogs"])
api_router.include_router(assets.router, prefix="/assets", tags=["assets"])
