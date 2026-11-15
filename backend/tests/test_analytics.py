import pytest
from app.analytics import analytics_engine

def test_nominal_risk_score():
    vitals = {
        "heart_rate": 68.0,
        "hrv": 66.0,
        "spo2": 98.8,
        "bp_systolic": 118.0,
        "bp_diastolic": 76.0,
        "core_temp": 36.7,
        "respiratory_rate": 13.0,
        "stress_index": 20.0,
        "sleep_quality": 88.0,
        "circadian_disruption_score": 12.0
    }
    baseline = {"baseline_hr": 68.0, "baseline_temp": 36.7}
    env = {"co2_ppm": 520.0, "cabin_pressure_kpa": 101.3, "o2_pct": 21.0}

    eval_result = analytics_engine.compute_composite_risk(vitals, baseline, env)
    assert "composite_risk_score" in eval_result
    assert eval_result["composite_risk_score"] < 30.0
    assert eval_result["risk_level"] in ["NOMINAL", "ELEVATED"]

def test_hypoxia_elevates_risk():
    vitals = {
        "heart_rate": 96.0,
        "hrv": 40.0,
        "spo2": 89.0, # Dangerous low oxygen
        "bp_systolic": 130.0,
        "bp_diastolic": 85.0,
        "core_temp": 36.9,
        "respiratory_rate": 22.0,
        "stress_index": 70.0,
        "sleep_quality": 50.0,
        "circadian_disruption_score": 30.0
    }
    baseline = {"baseline_hr": 68.0, "baseline_temp": 36.7}
    env = {"co2_ppm": 1400.0, "cabin_pressure_kpa": 98.0, "o2_pct": 19.5}

    eval_result = analytics_engine.compute_composite_risk(vitals, baseline, env)
    assert eval_result["composite_risk_score"] > 50.0
    assert "hypoxia" in eval_result["summary_explanation"].lower() or "cardiac" in eval_result["summary_explanation"].lower()

def test_metric_forecast():
    history = [70.0, 72.0, 75.0, 78.0, 82.0] # Rising trend
    fc = analytics_engine.forecast_metric(history, "heart_rate", 82.0, "bpm", warn_th=100.0, crit_th=125.0)
    assert fc["trend_direction"] == "RISING"
    assert len(fc["points"]) == 6 # 30 min / 5 min steps
    assert fc["points"][-1]["predicted_value"] > 82.0
