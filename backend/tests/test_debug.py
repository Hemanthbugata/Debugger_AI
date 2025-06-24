import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_debug_endpoint():
    response = client.post("/debug/", json={"error": "Sample error"})
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "fix" in data
    assert "sources" in data