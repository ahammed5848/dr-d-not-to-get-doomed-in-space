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

def test_research_summary():
    res = client.get("/api/research/summary")
    assert res.status_code == 200
    data = res.json()
    assert data["hazards_count"] == 5
    assert data["official_sources_count"] == 5
    assert "synthetic telemetry" in data["disclaimer"].lower()

def test_research_hazards():
    res = client.get("/api/research/hazards")
    assert res.status_code == 200
    hazards = res.json()
    assert len(hazards) == 5
    hazard_names = [h["name"] for h in hazards]
    assert "Space Radiation" in hazard_names
    assert "Isolation and Confinement" in hazard_names
    assert "Distance from Earth" in hazard_names
    assert "Altered Gravity Fields" in hazard_names
    assert "Hostile and Closed Environments" in hazard_names

def test_research_risks():
    res = client.get("/api/research/risks")
    assert res.status_code == 200
    risks = res.json()
    assert len(risks) >= 10
    
    # Filter by status
    res_filtered = client.get("/api/research/risks?status=MONITORED_IN_DR_D")
    assert res_filtered.status_code == 200
    for r in res_filtered.json():
        assert r["status"] == "MONITORED_IN_DR_D"

def test_research_evidence_reports():
    res = client.get("/api/research/evidence")
    assert res.status_code == 200
    reports = res.json()
    assert len(reports) >= 5
    
    # Search
    res_search = client.get("/api/research/evidence?search=CO2")
    assert res_search.status_code == 200
    assert len(res_search.json()) >= 1

def test_research_architecture():
    res = client.get("/api/research/architecture")
    assert res.status_code == 200
    arch = res.json()
    assert "HRP-48032" in arch["document_id"]
    assert len(arch["core_principles"]) >= 5

def test_research_eimo():
    res = client.get("/api/research/eimo")
    assert res.status_code == 200
    eimo = res.json()
    assert "20240001402" in eimo["document_id"]
    assert len(eimo["operational_pillars"]) >= 4

def test_research_conditions():
    res = client.get("/api/research/conditions")
    assert res.status_code == 200
    conditions = res.json()
    assert len(conditions) >= 10
    cond_names = [c["name"] for c in conditions]
    assert any("Hypercapnia" in n for n in cond_names)
    assert any("Hypoxia" in n for n in cond_names)

def test_research_sources():
    res = client.get("/api/research/sources")
    assert res.status_code == 200
    sources = res.json()
    assert len(sources) == 5
    for s in sources:
        assert "official_url" in s
        assert "provenance_tag" in s

def test_data_provenance():
    res = client.get("/api/research/provenance")
    assert res.status_code == 200
    prov = res.json()
    assert len(prov) == 5
    classifications = [p["classification"] for p in prov]
    assert "NASA Research Reference" in classifications
    assert "Synthetic Telemetry" in classifications
    assert "User-Imported CSV" in classifications
    assert "Model-Generated Output" in classifications
    assert "Third-Party Library or Service" in classifications

def test_research_event_context():
    res = client.get("/api/research/context/co2_spike")
    assert res.status_code == 200
    ctx = res.json()
    assert ctx["nasa_hazard"] == "Hostile and Closed Environments"
    assert "Synthetic Telemetry" in ctx["data_source"]

    res_rad = client.get("/api/research/context/radiation_storm")
    assert res_rad.status_code == 200
    ctx_rad = res_rad.json()
    assert ctx_rad["nasa_hazard"] == "Space Radiation"

def test_alerts_include_research_context():
    token = get_token("surgeon")
    res = client.get("/api/alerts?limit=5", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    alerts = res.json()
    assert len(alerts) > 0
    first_alert = alerts[0]
    assert "research_context" in first_alert
    assert first_alert["research_context"] is not None
    assert "nasa_hazard" in first_alert["research_context"]
