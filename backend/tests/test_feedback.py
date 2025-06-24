import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_feedback_endpoint():
    feedback = {
        "debug_request": {"error": "Sample error"},
        "response": {"summary": "Sample summary"},
        "rating": 5,
        "comment": "Very helpful!"
    }
    response = client.post("/feedback/", json=feedback)
    assert response.status_code == 200
    assert response.json()["status"] == "received"