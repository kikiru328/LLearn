import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.api.health import router


@pytest.fixture
def test_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(test_app: FastAPI) -> TestClient:
    return TestClient(test_app)


class TestHealthCheck:
    def test_basic_health_check_returns_200(self, client: TestClient) -> None:
        response = client.get("/health")
        assert response.status_code == 200

    def testr_basic_health_check_response_structure(self, client: TestClient) -> None:
        response = client.get("/health")
        data = response.json()

        assert "status" in data
        assert "timestamp" in data
        assert "service" in data
        assert "version" in data
        assert data["status"] == "healthy"
        assert data["service"] == "LLearn API"
        assert data["version"] == "1.0.0"

    def test_detailed_health_check_returns_200(self, client: TestClient) -> None:
        response = client.get("/health/detailed")
        assert response.status_code == 200

    def test_detailed_health_check_response_structure(self, client: TestClient) -> None:
        response = client.get("/health/detailed")
        data = response.json()

        assert "status" in data
        assert "timestamp" in data
        assert data["status"] == "healthy"
        assert "service" in data
        assert "name" in data["service"]
        assert "version" in data["service"]
        assert "environment" in data["service"]
        assert "system" in data
        assert "platform" in data["system"]
        assert "python_version" in data["system"]
        assert "architecture" in data["system"]
        assert "dependencies" in data
        assert "database" in data["dependencies"]
        assert "llm_service" in data["dependencies"]
