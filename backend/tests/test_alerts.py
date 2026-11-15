import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_token(username="surgeon"):
    res = client.post("/api/auth/login", json={
        "username": username,
        "password": "Password123!"
    })
    return res.json()["access_token"]

def test_get_alerts():
    token = get_token("surgeon")
    res = client.get("/api/alerts", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    alerts = res.json()
    assert isinstance(alerts, list)

def test_acknowledge_alert():
    token = get_token("surgeon")
    alerts_res = client.get("/api/alerts", headers={"Authorization": f"Bearer {token}"})
    alerts = alerts_res.json()
    if alerts:
        target_id = alerts[0]["id"]
        patch_res = client.patch(
            f"/api/alerts/{target_id}",
            json={"status": "ACKNOWLEDGED", "notes": "Telemetry reviewed by Flight Surgeon."},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert patch_res.status_code == 200
        assert patch_res.json()["status"] == "ACKNOWLEDGED"
