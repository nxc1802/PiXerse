"""
Test configuration and fixtures
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.base import Base, get_db
from app.models.base import Base  # Import to register all models
from main import app

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test"""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create test client with overridden database"""
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up
    app.dependency_overrides.clear()


@pytest.fixture
def sample_project_data():
    """Sample project data for testing"""
    return {
        "project_name": "Test Project",
        "description": "A test project for unit testing"
    }


@pytest.fixture
def sample_member_data():
    """Sample member data for testing"""
    return {
        "project_id": 1,
        "team_type": "Development",
        "role": "Frontend Developer",
        "experience": 2,
        "summary": "Test member summary"
    }


@pytest.fixture
def sample_blog_data():
    """Sample blog data for testing"""
    return {
        "project_id": 1,
        "title": "Test Blog Post",
        "detail": "This is a test blog post content"
    }


@pytest.fixture
def sample_asset_data():
    """Sample asset data for testing"""
    return {
        "filename": "test_image",
        "original_filename": "test_image.jpg",
        "cloudinary_public_id": "test/test_image_123",
        "cloudinary_url": "https://res.cloudinary.com/test/image/upload/test_image_123.jpg",
        "cloudinary_secure_url": "https://res.cloudinary.com/test/image/upload/test_image_123.jpg",
        "asset_type": "image",
        "file_size": 1024,
        "mime_type": "image/jpeg",
        "width": 800,
        "height": 600
    }
