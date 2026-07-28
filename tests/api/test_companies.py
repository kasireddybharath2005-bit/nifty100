from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_get_all_companies():
    response = client.get("/api/v1/companies")

    assert response.status_code == 200

    data = response.json()

    assert len(data["companies"]) > 0


def test_single_company():
    response = client.get("/api/v1/companies/TCS")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == "TCS"


def test_invalid_company():
    response = client.get("/api/v1/companies/INVALID")

    assert response.status_code == 404
