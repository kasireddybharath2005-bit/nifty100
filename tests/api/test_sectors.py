from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_get_sectors():
    response = client.get("/api/v1/sectors")

    assert response.status_code == 200

    data = response.json()

    assert len(data["sectors"]) > 0


def test_sector_companies():
    response = client.get("/api/v1/sectors/Information Technology/companies")

    assert response.status_code == 200

    data = response.json()

    assert len(data["companies"]) >= 0


def test_invalid_sector():
    response = client.get("/api/v1/sectors/INVALID/companies")

    assert response.status_code in [404, 200]
