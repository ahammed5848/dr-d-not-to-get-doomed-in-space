import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_success():
    response = client.post("/api/auth/login", json={
        "username": "surgeon",
        "password": "Password123!"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["role"] == "surgeon"

def test_login_invalid_password():
    response = client.post("/api/auth/login", json={
        "username": "surgeon",
        "password": "WrongPassword!"
    })
    assert response.status_code == 401

def test_get_me_with_token():
    # Login
    login_res = client.post("/api/auth/login", json={
        "username": "schen",
        "password": "Password123!"
    })
    token = login_res.json()["access_token"]
    
    # Get me
    me_res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    assert me_res.json()["username"] == "schen"
    assert me_res.json()["role"] == "astronaut"
