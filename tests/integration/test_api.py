from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_analyze_review_success():
    response = client.post("/api/v1/reviews", json={"text": "Very good product overall, works as intended."})
    assert response.status_code == 200
    data = response.json()
    assert "sentiment" in data
    assert "readability_score" in data
    assert "suggestions" in data
    assert isinstance(data["suggestions"], list)
    assert data["sentiment"] == "positive"
    assert isinstance(data["readability_score"], float)


def test_analyze_review_negative():
    response = client.post("/api/v1/reviews", json={"text": "Terrible product, very bad quality."})
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] == "negative"


def test_analyze_review_neutral():
    response = client.post("/api/v1/reviews", json={"text": "Product works as expected."})
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] == "neutral"


def test_analyze_review_suggestions():
    response = client.post("/api/v1/reviews", json={"text": "OK!!!!!!"})
    assert response.status_code == 200
    data = response.json()
    assert "Add more details to your review." in data["suggestions"]
    assert "Avoid excessive exclamation marks." in data["suggestions"]


def test_analyze_review_validation_error():
    response = client.post("/api/v1/reviews", json={"text": ""})
    assert response.status_code == 422


def test_analyze_review_invalid_json():
    response = client.post("/api/v1/reviews", json={})
    assert response.status_code == 422


def test_analyze_review_invalid_endpoint():
    response = client.post("/api/v1/invalid", json={"text": "test"})
    assert response.status_code == 404
