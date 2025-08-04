import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient

from app.main import app


class TestMonitoring:
    
    def test_healthcheck_sync(self):
        """Test healthcheck endpoint with sync client"""
        client = TestClient(app)
        response = client.get("/api/v1/monitoring/healthcheck/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["message"] == "Service is running"
    
    @pytest.mark.asyncio
    async def test_healthcheck_async(self, async_client: AsyncClient):
        """Test healthcheck endpoint with async client"""
        response = await async_client.get("/api/v1/monitoring/healthcheck/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["message"] == "Service is running"
