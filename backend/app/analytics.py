import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime, timezone, timedelta

class DrDAnalytics:
    def __init__(self):
        # Isolation Forest for multi-variable anomaly detection
        self.model = IsolationForest(
            n_estimators=100,
            contamination=0.05,
            random_state=42
        )
        self.is_fitted = False
        self._fit_default_model()

    def _fit_default_model(self):
        """Fit Isolation Forest on typical normal microgravity astronaut data"""
        np.random.seed(42)
        n_samples = 300
        # Features: [heart_rate, hrv, spo2, bp_sys, bp_dia, core_temp, resp_rate, stress_index]
        normal_data = np.column_stack([
            np.random.normal(68, 6, n_samples),     # HR
            np.random.normal(65, 10, n_samples),    # HRV
            np.random.normal(98.5, 0.8, n_samples), # SpO2
            np.random.normal(118, 7, n_samples),    # BP Sys
            np.random.normal(76, 5, n_samples),     # BP Dia
            np.random.normal(36.8, 0.25, n_samples),# Temp
            np.random.normal(14, 1.8, n_samples),   # Resp
            np.random.normal(25, 8, n_samples),     # Stress
        ])
        self.model.fit(normal_data)
        self.is_fitted = True

    def evaluate_multi_variable_anomaly(self, reading: Dict[str, float]) -> Tuple[bool, float]:
        """
        Uses Isolation Forest. Returns (is_anomaly, anomaly_score_0_to_1).
        IsolationForest decision_function returns lower values for anomalies.
        """
        features = np.array([[
            reading.get("heart_rate", 70.0),
            reading.get("hrv", 60.0),
            reading.get("spo2", 98.0),
            reading.get("bp_systolic", 120.0),
            reading.get("bp_diastolic", 80.0),
            reading.get("core_temp", 36.8),
            reading.get("respiratory_rate", 14.0),
            reading.get("stress_index", 25.0)
        ]])
        score_raw = self.model.decision_function(features)[0] # typical range [-0.2, 0.2]
        pred = self.model.predict(features)[0] # -1 for anomaly, 1 for normal

        # Normalize raw score to 0 (normal) - 100 (high anomaly)
        anomaly_metric = max(0.0, min(100.0, (0.15 - score_raw) * 250.0))
        return (pred == -1, round(anomaly_metric, 1))

    def compute_z_score_baseline(self, current_val: float, baseline_mean: float, std: float = 5.0) -> float:
        """Returns standard z-score relative to personal baseline"""
        if std <= 0:
            std = 1.0
        return (current_val - baseline_mean) / std

    def compute_composite_risk(
        self,
        vitals: Dict[str, Any],
        baseline: Dict[str, float],
        environment: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Computes 0-100 composite Health Risk Index with explainable factor breakdown.
        """
        factors = []
        cardio_score = 0.0
        hypoxia_score = 0.0
        thermal_score = 0.0
        stress_score = 0.0
        env_score = 0.0

        hr = vitals.get("heart_rate", 70.0)
        hrv = vitals.get("hrv", 60.0)
        spo2 = vitals.get("spo2", 98.5)
        bp_sys = vitals.get("bp_systolic", 120.0)
        bp_dia = vitals.get("bp_diastolic", 80.0)
        temp = vitals.get("core_temp", 36.8)
        resp = vitals.get("respiratory_rate", 14.0)
        stress = vitals.get("stress_index", 20.0)
        sleep_q = vitals.get("sleep_quality", 85.0)
        circadian = vitals.get("circadian_disruption_score", 15.0)

        # 1. Cardio factor (HR, BP, HRV)
        hr_base = baseline.get("baseline_hr", 68.0)
        hr_diff = abs(hr - hr_base)
        if hr > 110:
            cardio_score += min(50.0, (hr - 100) * 1.5)
        elif hr < 48:
            cardio_score += min(50.0, (50 - hr) * 2.5)

        if bp_sys > 135:
            cardio_score += min(25.0, (bp_sys - 130) * 1.2)
        if hrv < 30:
            cardio_score += min(25.0, (35 - hrv) * 1.5)
        cardio_score = min(100.0, cardio_score)

        cardio_impact = "LOW"
        if cardio_score > 60: cardio_impact = "CRITICAL"
        elif cardio_score > 35: cardio_impact = "HIGH"
        elif cardio_score > 15: cardio_impact = "MEDIUM"

        cardio_detail = f"HR {hr:.0f} bpm (baseline: {hr_base:.0f}), HRV {hrv:.0f} ms"
        factors.append({
            "name": "Cardiovascular Autonomic Load",
            "score": round(cardio_score, 1),
            "impact": cardio_impact,
            "detail": cardio_detail
        })

        # 2. Hypoxia / Respiratory factor
        if spo2 < 96.0:
            hypoxia_score += (96.0 - spo2) * 18.0
        if resp > 20:
            hypoxia_score += (resp - 20) * 4.0
        elif resp < 10:
            hypoxia_score += (10 - resp) * 6.0
        hypoxia_score = min(100.0, hypoxia_score)

        hypoxia_impact = "LOW"
        if hypoxia_score > 60: hypoxia_impact = "CRITICAL"
        elif hypoxia_score > 35: hypoxia_impact = "HIGH"
        elif hypoxia_score > 15: hypoxia_impact = "MEDIUM"

        factors.append({
            "name": "Oxygen Saturation & Ventilation",
            "score": round(hypoxia_score, 1),
            "impact": hypoxia_impact,
            "detail": f"SpO2 {spo2:.1f}%, Resp {resp:.0f} br/min"
        })

        # 3. Thermal factor
        t_base = baseline.get("baseline_temp", 36.8)
        temp_diff = abs(temp - t_base)
        if temp > 37.6:
            thermal_score = min(100.0, (temp - 37.5) * 65.0)
        elif temp < 36.0:
            thermal_score = min(100.0, (36.0 - temp) * 75.0)

        thermal_impact = "LOW"
        if thermal_score > 60: thermal_impact = "CRITICAL"
        elif thermal_score > 35: thermal_impact = "HIGH"
        elif thermal_score > 15: thermal_impact = "MEDIUM"

        factors.append({
            "name": "Thermoregulatory Core Stability",
            "score": round(thermal_score, 1),
            "impact": thermal_impact,
            "detail": f"Core temp {temp:.2f} °C (baseline: {t_base:.1f} °C)"
        })

        # 4. Stress, Neuro & Circadian
        stress_score = stress * 0.45 + circadian * 0.35 + (100.0 - sleep_q) * 0.20
        stress_score = min(100.0, stress_score)

        stress_impact = "LOW"
        if stress_score > 65: stress_impact = "CRITICAL"
        elif stress_score > 45: stress_impact = "HIGH"
        elif stress_score > 25: stress_impact = "MEDIUM"

        factors.append({
            "name": "Stress & Circadian Rhythm Disruption",
            "score": round(stress_score, 1),
            "impact": stress_impact,
            "detail": f"Stress {stress:.0f}/100, Circadian lag {circadian:.0f}/100, Sleep Q {sleep_q:.0f}%"
        })

        # 5. Environment Correlation (CO2, cabin pressure)
        if environment:
            co2 = environment.get("co2_ppm", 520.0)
            p_kpa = environment.get("cabin_pressure_kpa", 101.3)
            o2_pct = environment.get("o2_pct", 21.0)

            if co2 > 800:
                env_score += min(60.0, (co2 - 800) / 25.0)
            if p_kpa < 95.0:
                env_score += (95.0 - p_kpa) * 6.0
            if o2_pct < 20.0:
                env_score += (20.0 - o2_pct) * 20.0
            env_score = min(100.0, env_score)

            env_impact = "LOW"
            if env_score > 60: env_impact = "CRITICAL"
            elif env_score > 35: env_impact = "HIGH"
            elif env_score > 15: env_impact = "MEDIUM"

            factors.append({
                "name": "Spacecraft Environmental Strain",
                "score": round(env_score, 1),
                "impact": env_impact,
                "detail": f"Cabin CO2 {co2:.0f} ppm, Pressure {p_kpa:.1f} kPa, O2 {o2_pct:.1f}%"
            })

        # Isolation Forest multi-variable check
        is_if_anomaly, if_score = self.evaluate_multi_variable_anomaly(vitals)

        # Composite Risk Formula (Weighted average with peak amplifier)
        weights = [0.28, 0.28, 0.16, 0.14, 0.14]
        factor_scores = [cardio_score, hypoxia_score, thermal_score, stress_score, env_score]
        weighted_sum = sum(w * s for w, s in zip(weights, factor_scores))

        # Peak factor amplifies overall risk (e.g. if one vital is severely compromised)
        peak_factor = max(factor_scores)
        composite = 0.60 * weighted_sum + 0.35 * peak_factor + 0.05 * if_score
        composite = min(100.0, max(0.0, composite))

        # Determine level & explanation
        risk_level = "NOMINAL"
        if composite >= 75.0: risk_level = "SEVERE"
        elif composite >= 50.0: risk_level = "HIGH"
        elif composite >= 25.0: risk_level = "ELEVATED"

        # Generate human-explainable breakdown
        elevated_reasons = []
        if hypoxia_score > 25: elevated_reasons.append(f"hypoxia risk (SpO2 {spo2:.1f}%)")
        if cardio_score > 25: elevated_reasons.append(f"cardiac strain ({hr:.0f} bpm)")
        if env_score > 25: elevated_reasons.append("elevated cabin CO2")
        if thermal_score > 25: elevated_reasons.append(f"core thermal variation ({temp:.2f}°C)")
        if stress_score > 40: elevated_reasons.append("cumulative circadian/stress fatigue")

        if elevated_reasons:
            explanation = "Risk elevated due to " + " + ".join(elevated_reasons) + "."
            action = "Initiate telemetry watch, verify life support scrubbers, and advise crew rest."
        else:
            explanation = "Physiological vitals nominal. Autonomic and environmental parameters stable."
            action = "Maintain standard mission schedule and hydration countermeasure."

        return {
            "composite_risk_score": round(composite, 1),
            "risk_level": risk_level,
            "factors": factors,
            "summary_explanation": explanation,
            "recommended_action": action,
            "is_anomaly": is_if_anomaly
        }

    def forecast_metric(
        self,
        historical_values: List[float],
        metric_name: str,
        current_value: float,
        unit: str,
        warn_th: Optional[float] = None,
        crit_th: Optional[float] = None,
        horizon_minutes: int = 30,
        interval_minutes: int = 5
    ) -> Dict[str, Any]:
        """
        Predicts future values over next 30 minutes using linear trend + exponential smoothing.
        """
        if not historical_values:
            historical_values = [current_value] * 5

        y = np.array(historical_values)
        x = np.arange(len(y))

        # Linear regression slope
        if len(y) > 1:
            slope, intercept = np.polyfit(x, y, 1)
        else:
            slope = 0.0

        # Dampened slope for realistic physiology
        dampened_slope = slope * 0.75

        # Trend direction
        direction = "STABLE"
        if abs(dampened_slope) > 0.05:
            direction = "RISING" if dampened_slope > 0 else "FALLING"

        points = []
        num_steps = horizon_minutes // interval_minutes
        now = datetime.now(timezone.utc)

        for step in range(1, num_steps + 1):
            future_min = step * interval_minutes
            t_future = (now + timedelta(minutes=future_min)).strftime("%H:%M")
            # Projected value
            projected = current_value + dampened_slope * (step * 0.8)

            # Physiological clipping
            if metric_name == "spo2":
                projected = min(100.0, max(75.0, projected))
            elif metric_name == "heart_rate":
                projected = max(35.0, min(190.0, projected))
            elif metric_name == "core_temp":
                projected = max(34.0, min(41.0, projected))
            elif metric_name == "co2_ppm":
                projected = max(350.0, projected)

            # Uncertainty expands with time
            margin = 0.03 * current_value * (step / num_steps)
            lower = projected - margin
            upper = projected + margin

            # Breach check
            breach_warn = False
            breach_crit = False
            if warn_th is not None:
                if (direction == "RISING" and projected >= warn_th) or (direction == "FALLING" and projected <= warn_th):
                    breach_warn = True
            if crit_th is not None:
                if (direction == "RISING" and projected >= crit_th) or (direction == "FALLING" and projected <= crit_th):
                    breach_crit = True

            points.append({
                "timestamp": f"+{future_min}m ({t_future})",
                "predicted_value": round(projected, 1),
                "lower_bound": round(lower, 1),
                "upper_bound": round(upper, 1),
                "breach_warning": breach_warn,
                "breach_critical": breach_crit
            })

        return {
            "metric": metric_name,
            "current_value": round(current_value, 1),
            "unit": unit,
            "trend_direction": direction,
            "points": points,
            "warning_threshold": warn_th,
            "critical_threshold": crit_th
        }

analytics_engine = DrDAnalytics()
