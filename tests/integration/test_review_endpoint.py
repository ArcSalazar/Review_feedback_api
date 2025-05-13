from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_analyze_review_success():
    response = client.post(
        "/api/v1/reviews/",
        json={"text": "Test review"}
    )
    assert response.status_code == 200
    assert "sentiment" in response.json()
    assert "readability_score" in response.json()
    assert "suggestions" in response.json()


def test_analyze_review_empty():
    response = client.post(
        "/api/v1/reviews/",
        json={"text": ""}
    )
    assert response.status_code == 422


def test_analyze_review_invalid_json():
    response = client.post(
        "/api/v1/reviews/",
        json={}
    )
    assert response.status_code == 422


def test_analyze_review_positive():
    response = client.post(
        "/api/v1/reviews/",
        json={"text": "Great product, excellent quality!"}
    )
    assert response.status_code == 200
    assert response.json()["sentiment"] == "positive"


def test_analyze_review_negative():
    response = client.post(
        "/api/v1/reviews/",
        json={"text": "Terrible product, very poor quality"}
    )
    assert response.status_code == 200
    assert response.json()["sentiment"] == "negative"


def test_analyze_review_suggestions():
    response = client.post(
        "/api/v1/reviews/",
        json={"text": "OK!!!!!!!"}
    )
    assert response.status_code == 200
    suggestions = response.json()["suggestions"]
    assert "Add more details to your review." in suggestions
    assert "Avoid excessive exclamation marks." in suggestions
