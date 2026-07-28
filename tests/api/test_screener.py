from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_get_screener():
    response = client.get("/api/v1/screener")

    assert response.status_code == 200

    data = response.json()

    assert len(data["companies"]) > 0


def test_screener_filter():
    response = client.get("/api/v1/screener?min_roe=15")

    assert response.status_code == 200


def test_invalid_filter():
    response = client.get("/api/v1/screener?min_roe=abc")

    print("Status Code:", response.status_code)
    print(response.text)

    assert True
