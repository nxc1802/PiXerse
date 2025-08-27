"""
Base models and imports
"""

from app.database.base import Base

# Import all models here to ensure they are registered with SQLAlchemy
from app.models.project import Project  # noqa: F401
from app.models.member import Member  # noqa: F401  
from app.models.blog import Blog  # noqa: F401
from app.models.asset import Asset  # noqa: F401
from app.models.associations import *  # noqa: F401, F403

__all__ = ["Base"]
