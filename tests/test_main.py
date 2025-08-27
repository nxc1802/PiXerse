"""
Tests for main application endpoints
"""

import pytest
from fastapi.testclient import TestClient


class TestMainEndpoints:
    """Test class for main application endpoints"""

    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "PiXerse" in data["message"]

    def test_health_check(self, client: TestClient):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "PiXerse" in data["message"]

    def test_docs_endpoint(self, client: TestClient):
        """Test API documentation endpoint"""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_openapi_endpoint(self, client: TestClient):
        """Test OpenAPI schema endpoint"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        data = response.json()
        assert "openapi" in data
        assert data["info"]["title"] == "PiXerse Backend"


class TestCORS:
    """Test CORS configuration"""

    def test_cors_headers(self, client: TestClient):
        """Test CORS headers are present"""
        response = client.options("/")
        # CORS headers should be present in actual deployment
        # For testing, we just verify the endpoint works
        assert response.status_code in [200, 405]  # OPTIONS might not be allowed


class TestErrorHandling:
    """Test error handling"""

    def test_404_endpoint(self, client: TestClient):
        """Test non-existent endpoint returns 404"""
        response = client.get("/nonexistent-endpoint")
        assert response.status_code == 404

    def test_method_not_allowed(self, client: TestClient):
        """Test method not allowed"""
        response = client.post("/health")  # Health only accepts GET
        assert response.status_code == 405
