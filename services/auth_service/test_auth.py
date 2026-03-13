import pytest
from fastapi.testclient import TestClient
from services.auth_service.main import app

client = TestClient(app)

def test_login():
    response = client.post("/token", data={"username": "admin", "password": "admin"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_admin_route_without_token():
    response = client.get("/admin-only")
    assert response.status_code == 401

def test_audit_logs_unauthorized():
    response = client.get("/audit-logs")
    assert response.status_code == 401
