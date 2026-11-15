import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.routers.auth import FAILED_ATTEMPTS

client = TestClient(app)

def test_login_rate_limiting():
    # Clear any leftover failures for test isolation
    FAILED_ATTEMPTS.clear()
    
    # 5 failed attempts
    for _ in range(5):
        res = client.post("/api/auth/login", json={
            "username": "admin",
            "password": "WrongPasswordAttempt"
        })
        assert res.status_code == 401
    
    # 6th attempt should hit rate limit (HTTP 429)
    res_limited = client.post("/api/auth/login", json={
        "username": "admin",
        "password": "Password123!"
    })
    assert res_limited.status_code == 429
    assert "Rate limit exceeded" in res_limited.json()["detail"]
    
    # Reset failures
    FAILED_ATTEMPTS.clear()

def test_threshold_boundary_validation():
    # Login as admin
    login_res = client.post("/api/auth/login", json={
        "username": "admin",
        "password": "Password123!"
    })
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Attempt warning_low > warning_high -> 422
    bad_res1 = client.put("/api/thresholds/heart_rate", json={
        "warning_low": 120.0,
        "warning_high": 100.0,
        "critical_low": 40.0,
        "critical_high": 140.0
    }, headers=headers)
    assert bad_res1.status_code == 422
    assert "warning_low" in bad_res1.json()["detail"]

    # Attempt critical_low > warning_low -> 422
    bad_res2 = client.put("/api/thresholds/heart_rate", json={
        "warning_low": 50.0,
        "warning_high": 100.0,
        "critical_low": 60.0,
        "critical_high": 140.0
    }, headers=headers)
    assert bad_res2.status_code == 422
    assert "critical_low" in bad_res2.json()["detail"]

    # Valid update -> 200
    good_res = client.put("/api/thresholds/heart_rate", json={
        "warning_low": 50.0,
        "warning_high": 100.0,
        "critical_low": 45.0,
        "critical_high": 130.0
    }, headers=headers)
    assert good_res.status_code == 200

def test_astronaut_rbac_scoping():
    # Login as astronaut schen (astronaut_id = 1)
    login_res = client.post("/api/auth/login", json={
        "username": "schen",
        "password": "Password123!"
    })
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Accessing self advisor -> 200
    res_self_advisor = client.get("/api/astronauts/1/advisor", headers=headers)
    assert res_self_advisor.status_code == 200

    # Accessing another astronaut's advisor (id = 2) -> 403 Forbidden
    res_other_advisor = client.get("/api/astronauts/2/advisor", headers=headers)
    assert res_other_advisor.status_code == 403

    # Accessing another astronaut's clinical notes (id = 2) -> 403 Forbidden
    res_other_notes = client.get("/api/astronauts/2/notes", headers=headers)
    assert res_other_notes.status_code == 403

def test_checkin_validation():
    # Login as astronaut schen
    login_res = client.post("/api/auth/login", json={
        "username": "schen",
        "password": "Password123!"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Invalid sleep hours (> 24) -> 422
    res_bad_sleep = client.post("/api/checkins", json={
        "astronaut_id": 1,
        "sleep_hours": 26.0,
        "sleep_quality_score": 7.0,
        "physical_fatigue": 3.0,
        "cognitive_fatigue": 3.0,
        "mood_score": 8.0,
        "muscle_soreness": 2.0,
        "headache_score": 1.0,
        "space_motion_sickness": 1.0,
        "comments": "Invalid sleep"
    }, headers=headers)
    assert res_bad_sleep.status_code == 422

    # Invalid score (> 10) -> 422
    res_bad_score = client.post("/api/checkins", json={
        "astronaut_id": 1,
        "sleep_hours": 7.5,
        "sleep_quality_score": 15.0,
        "physical_fatigue": 3.0,
        "cognitive_fatigue": 3.0,
        "mood_score": 8.0,
        "muscle_soreness": 2.0,
        "headache_score": 1.0,
        "space_motion_sickness": 1.0,
        "comments": "Score too high"
    }, headers=headers)
    assert res_bad_score.status_code == 422

    # Valid checkin -> 201 Created
    res_valid = client.post("/api/checkins", json={
        "astronaut_id": 1,
        "sleep_hours": 7.5,
        "sleep_quality_score": 8.0,
        "physical_fatigue": 3.0,
        "cognitive_fatigue": 3.0,
        "mood_score": 8.0,
        "muscle_soreness": 2.0,
        "headache_score": 1.0,
        "space_motion_sickness": 1.0,
        "comments": "Nominal rest"
    }, headers=headers)
    assert res_valid.status_code == 201
