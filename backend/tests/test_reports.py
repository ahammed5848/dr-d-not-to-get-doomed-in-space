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

def test_export_pdf_report():
    token = get_token("surgeon")
    res = client.get("/api/reports/1?format=pdf&hours=24", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.headers["content-type"] == "application/pdf"
    assert len(res.content) > 100 # Has generated PDF bytes

def test_export_csv_report():
    token = get_token("surgeon")
    res = client.get("/api/reports/1?format=csv&hours=24", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert "text/csv" in res.headers["content-type"]
    text = res.content.decode("utf-8")
    assert "DR D ASTRONAUT HEALTH REPORT" in text
    assert "Heart Rate (bpm)" in text

def test_astronaut_cannot_export_other_report():
    token = get_token("schen") # Sarah Chen is astronaut 1
    # Try exporting astronaut 2
    res = client.get("/api/reports/2?format=pdf&hours=24", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 403
