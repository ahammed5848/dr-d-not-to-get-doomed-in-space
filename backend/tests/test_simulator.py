import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_trigger_scenario():
    res = client.post("/api/simulation/scenario", json={
        "scenario_type": "co2_spike",
        "severity": "moderate"
    })
    assert res.status_code == 200
    assert res.json()["status"] == "triggered"

def test_set_simulation_speed():
    res = client.post("/api/simulation/speed", json={"speed": 10})
    assert res.status_code == 200
    assert res.json()["simulation_speed"] == 10

    # Reset speed
    client.post("/api/simulation/speed", json={"speed": 1})

def test_reset_simulation():
    res = client.post("/api/simulation/reset")
    assert res.status_code == 200
    assert res.json()["status"] == "success"
