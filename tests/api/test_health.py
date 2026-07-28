from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_health_status():
    response = client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


def test_database_connected():
    response = client.get("/api/v1/health")

    data = response.json()

    assert data["database"] == "connected"


def test_version():
    response = client.get("/api/v1/health")

    data = response.json()

    assert "version" in data


def test_uptime():
    response = client.get("/api/v1/health")

    data = response.json()

    assert "uptime_seconds" in data