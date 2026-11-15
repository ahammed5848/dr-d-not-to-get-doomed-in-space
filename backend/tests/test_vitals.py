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

def test_get_astronauts_surgeon():
    token = get_token("surgeon")
    res = client.get("/api/astronauts", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    crew = res.json()
    assert len(crew) == 4
    assert any(a["callsign"] == "Valkyrie" for a in crew)

def test_get_astronauts_astronaut_scoping():
    token = get_token("schen") # Sarah Chen is astro id 1
    res = client.get("/api/astronauts", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    crew = res.json()
    assert len(crew) == 1
    assert crew[0]["callsign"] == "Valkyrie"

def test_telemetry_ingestion():
    res = client.post("/api/telemetry", json={
        "astronaut_id": 1,
        "heart_rate": 74.0,
        "hrv": 62.0,
        "spo2": 98.4,
        "bp_systolic": 118.0,
        "bp_diastolic": 76.0,
        "core_temp": 36.8,
        "skin_temp": 33.4,
        "respiratory_rate": 14.0,
        "sleep_quality": 88.0,
        "stress_index": 18.0,
        "activity_level": "REST"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["heart_rate"] == 74.0
    assert data["astronaut_id"] == 1

def test_get_environment():
    res = client.get("/api/environment")
    assert res.status_code == 200
    data = res.json()
    assert len(data) > 0
    assert "co2_ppm" in data[0]
