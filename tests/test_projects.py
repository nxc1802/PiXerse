"""
Tests for Project API endpoints
"""

import pytest
from fastapi.testclient import TestClient
from app.models.project import Project


class TestProjectAPI:
    """Test class for Project API endpoints"""

    def test_create_project(self, client: TestClient, sample_project_data):
        """Test creating a new project"""
        response = client.post("/api/v1/projects/", json=sample_project_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["project_name"] == sample_project_data["project_name"]
        assert data["description"] == sample_project_data["description"]
        assert "project_id" in data
        assert "created_at" in data

    def test_get_projects(self, client: TestClient, sample_project_data):
        """Test getting list of projects"""
        # Create a project first
        client.post("/api/v1/projects/", json=sample_project_data)
        
        # Get projects
        response = client.get("/api/v1/projects/")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["project_name"] == sample_project_data["project_name"]

    def test_get_project_by_id(self, client: TestClient, sample_project_data):
        """Test getting a specific project by ID"""
        # Create a project
        create_response = client.post("/api/v1/projects/", json=sample_project_data)
        project_id = create_response.json()["project_id"]
        
        # Get project by ID
        response = client.get(f"/api/v1/projects/{project_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["project_id"] == project_id
        assert data["project_name"] == sample_project_data["project_name"]

    def test_get_nonexistent_project(self, client: TestClient):
        """Test getting a project that doesn't exist"""
        response = client.get("/api/v1/projects/999")
        assert response.status_code == 404

    def test_update_project(self, client: TestClient, sample_project_data):
        """Test updating a project"""
        # Create a project
        create_response = client.post("/api/v1/projects/", json=sample_project_data)
        project_id = create_response.json()["project_id"]
        
        # Update project
        update_data = {"project_name": "Updated Project Name"}
        response = client.patch(f"/api/v1/projects/{project_id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["project_name"] == "Updated Project Name"
        assert data["description"] == sample_project_data["description"]  # Should remain unchanged

    def test_update_nonexistent_project(self, client: TestClient):
        """Test updating a project that doesn't exist"""
        update_data = {"project_name": "Updated Name"}
        response = client.patch("/api/v1/projects/999", json=update_data)
        assert response.status_code == 404

    def test_delete_project(self, client: TestClient, sample_project_data):
        """Test deleting a project"""
        # Create a project
        create_response = client.post("/api/v1/projects/", json=sample_project_data)
        project_id = create_response.json()["project_id"]
        
        # Delete project
        response = client.delete(f"/api/v1/projects/{project_id}")
        assert response.status_code == 200
        
        # Verify project is deleted
        get_response = client.get(f"/api/v1/projects/{project_id}")
        assert get_response.status_code == 404

    def test_delete_nonexistent_project(self, client: TestClient):
        """Test deleting a project that doesn't exist"""
        response = client.delete("/api/v1/projects/999")
        assert response.status_code == 404

    def test_project_name_validation(self, client: TestClient):
        """Test project name validation"""
        # Test empty project name
        invalid_data = {"project_name": "", "description": "Test"}
        response = client.post("/api/v1/projects/", json=invalid_data)
        assert response.status_code == 422  # Validation error

    def test_projects_pagination(self, client: TestClient):
        """Test projects pagination"""
        # Create multiple projects
        for i in range(5):
            project_data = {
                "project_name": f"Project {i}",
                "description": f"Description {i}"
            }
            client.post("/api/v1/projects/", json=project_data)
        
        # Test pagination
        response = client.get("/api/v1/projects/?skip=2&limit=2")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 2
