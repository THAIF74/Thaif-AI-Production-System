from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_process_text():
    response = client.post(
        "/process",
        json={"text": "Hello   world"},
    )
    assert response.status_code == 200
    assert response.json()["word_count"] == 2
    assert response.json()["uppercase_text"] == "HELLO WORLD"
    assert response.json()["status"] == "processed"


def test_empty_text_rejected():
    response = client.post("/process", json={"text": "   "})
    assert response.status_code == 422


def test_request_id_header():
    response = client.get("/health")
    assert response.headers.get("X-Request-ID")


def test_invalid_payload_rejected():
    response = client.post("/process", json={"text": ""})
    assert response.status_code == 422