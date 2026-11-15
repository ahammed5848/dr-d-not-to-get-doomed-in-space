import pytest
import io
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ingest_telemetry_batch():
    batch = [
        {
            "astronaut_id": 1,
            "heart_rate": 72.0,
            "hrv": 64.0,
            "spo2": 98.6,
            "bp_systolic": 118.0,
            "bp_diastolic": 76.0,
            "core_temp": 36.8,
            "skin_temp": 33.4,
            "respiratory_rate": 13.0,
            "sleep_quality": 88.0,
            "stress_index": 19.0,
            "activity_level": "REST"
        },
        {
            "astronaut_id": 2,
            "heart_rate": 70.0,
            "hrv": 60.0,
            "spo2": 98.2,
            "bp_systolic": 120.0,
            "bp_diastolic": 78.0,
            "core_temp": 36.7,
            "skin_temp": 33.5,
            "respiratory_rate": 14.0,
            "sleep_quality": 85.0,
            "stress_index": 22.0,
            "activity_level": "REST"
        }
    ]
    res = client.post("/api/telemetry/batch", json=batch)
    assert res.status_code == 200
    assert res.json()["status"] == "success"
    assert res.json()["ingested_count"] == 2

def test_ingest_telemetry_csv():
    csv_content = """astronaut_id,heart_rate,hrv,spo2,bp_systolic,bp_diastolic,core_temp,skin_temp,respiratory_rate,stress_index,activity_level
1,75.0,60.0,98.5,118.0,76.0,36.7,33.4,14.0,20.0,REST
2,78.0,58.0,98.0,122.0,78.0,36.8,33.5,15.0,24.0,REST
"""
    files = {"file": ("test_telemetry.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")}
    res = client.post("/api/telemetry/csv", files=files)
    assert res.status_code == 200
    assert res.json()["status"] == "success"
    assert res.json()["records_ingested"] == 2
