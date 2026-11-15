import asyncio
import math
import random
import time
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List, Callable
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import (
    Astronaut, VitalReading, EnvironmentReading, Alert,
    Threshold, RiskSnapshot
)
from .analytics import analytics_engine

class DrDSimulator:
    def __init__(self):
        self.speed: int = 1 # 1x, 10x, 60x
        self.is_running: bool = False
        self.active_scenarios: Dict[str, Dict[str, Any]] = {}
        # active_scenarios key: scenario_name or "astro_{id}"
        # value: {type, target_astronaut_id, start_time, duration_seconds, progress}
        self.listeners: List[Callable[[Dict[str, Any]], Any]] = []
        self.tick_count: int = 0
        self.lock = asyncio.Lock()

        # Simulated spacecraft cabin state
        self.cabin_co2: float = 520.0
        self.cabin_o2: float = 21.2
        self.cabin_temp: float = 22.4
        self.cabin_humidity: float = 44.0
        self.cabin_pressure: float = 101.3
        self.cabin_noise: float = 58.2

    def add_listener(self, callback: Callable[[Dict[str, Any]], Any]):
        if callback not in self.listeners:
            self.listeners.append(callback)

    def remove_listener(self, callback: Callable[[Dict[str, Any]], Any]):
        if callback in self.listeners:
            self.listeners.remove(callback)

    def trigger_scenario(self, scenario_type: str, astronaut_id: Optional[int] = None, severity: str = "moderate"):
        """Triggers a dynamic demo scenario with auto-recovery"""
        scenario_key = f"astro_{astronaut_id}" if astronaut_id else "global"
        
        if scenario_type == "nominal":
            # Clear all or specific
            if scenario_key in self.active_scenarios:
                del self.active_scenarios[scenario_key]
            else:
                self.active_scenarios.clear()
            return {"status": "cleared", "scenario": "nominal"}

        duration = 60 # Default 60 seconds duration before auto-decay
        if severity == "severe":
            duration = 120
        elif severity == "mild":
            duration = 40

        self.active_scenarios[scenario_key] = {
            "type": scenario_type,
            "target_astronaut_id": astronaut_id or 1, # Default to primary if not specified
            "severity": severity,
            "start_time": time.time(),
            "duration": duration,
            "decay_started": False
        }
        return {
            "status": "triggered",
            "scenario": scenario_type,
            "target_astronaut_id": astronaut_id,
            "severity": severity,
            "duration_sec": duration
        }

    def set_speed(self, speed: int):
        self.speed = max(1, min(100, speed))
        return {"simulation_speed": self.speed}

    def get_active_scenarios_list(self) -> List[str]:
        return [f"{v['type']} (target: Astro {v['target_astronaut_id']})" for v in self.active_scenarios.values()]

    async def step(self, db: Session):
        """Execute one simulation cycle"""
        self.tick_count += 1
        now = datetime.now(timezone.utc)
        current_time_sec = time.time()

        # Update Cabin Environment
        env_scenario = any(s["type"] == "co2_spike" for s in self.active_scenarios.values())
        if env_scenario:
            # Rapid rise
            self.cabin_co2 = min(2200.0, self.cabin_co2 + 45.0)
            self.cabin_o2 = max(19.2, self.cabin_o2 - 0.05)
            self.cabin_temp = min(25.8, self.cabin_temp + 0.08)
        else:
            # Return towards nominal
            target_co2 = 520.0 + 25.0 * math.sin(self.tick_count / 15.0)
            self.cabin_co2 += (target_co2 - self.cabin_co2) * 0.15
            self.cabin_o2 += (21.2 - self.cabin_o2) * 0.1
            self.cabin_temp += (22.4 - self.cabin_temp) * 0.1

        # Add natural sensor fluctuation
        env_reading = EnvironmentReading(
            timestamp=now,
            co2_ppm=round(self.cabin_co2 + random.uniform(-6, 6), 1),
            o2_pct=round(self.cabin_o2 + random.uniform(-0.04, 0.04), 2),
            cabin_temp_c=round(self.cabin_temp + random.uniform(-0.1, 0.1), 2),
            humidity_pct=round(self.cabin_humidity + random.uniform(-0.5, 0.5), 1),
            cabin_pressure_kpa=round(self.cabin_pressure + random.uniform(-0.1, 0.1), 1),
            noise_db=round(self.cabin_noise + random.uniform(-1.0, 1.5), 1)
        )
        db.add(env_reading)

        # Check Cabin Alerts
        if env_reading.co2_ppm > 1500:
            existing_active = db.query(Alert).filter(
                Alert.metric == "co2_ppm", Alert.status == "ACTIVE"
            ).first()
            if not existing_active:
                alert = Alert(
                    timestamp=now,
                    metric="co2_ppm",
                    value=env_reading.co2_ppm,
                    threshold_level="CRITICAL" if env_reading.co2_ppm > 1800 else "WARNING",
                    message=f"Cabin atmospheric CO2 reached dangerous level ({env_reading.co2_ppm:.0f} ppm)",
                    suggested_action="Command Life Support LiOH scrubbers to HIGH. Don oxygen masks if >2000 ppm.",
                    status="ACTIVE"
                )
                db.add(alert)

        # Process each astronaut
        astronauts = db.query(Astronaut).all()
        broadcast_vitals = []
        new_alerts = []

        # Check expired scenarios
        expired_keys = []
        for k, sc in self.active_scenarios.items():
            elapsed = current_time_sec - sc["start_time"]
            if elapsed > sc["duration"]:
                expired_keys.append(k)
        for k in expired_keys:
            del self.active_scenarios[k]

        for astro in astronauts:
            # Check if this astronaut is target of a scenario
            active_sc = None
            for sc in self.active_scenarios.values():
                if sc.get("target_astronaut_id") == astro.id:
                    active_sc = sc["type"]
                    break
            
            # Global scenarios affect all
            if not active_sc and env_scenario:
                active_sc = "co2_spike_crew"

            # Baseline calculations with circadian sine wave (24h period simulated)
            circadian_wave = math.sin(self.tick_count * 0.05 + astro.id)
            hr = astro.baseline_hr + 3.0 * circadian_wave + random.uniform(-1.5, 1.5)
            hrv = astro.baseline_hrv + random.uniform(-2, 2)
            spo2 = astro.baseline_spo2 + random.uniform(-0.2, 0.2)
            bp_sys = astro.baseline_bp_sys + 2.0 * circadian_wave + random.uniform(-1.5, 1.5)
            bp_dia = astro.baseline_bp_dia + 1.0 * circadian_wave + random.uniform(-1.0, 1.0)
            core_t = astro.baseline_temp + 0.1 * circadian_wave + random.uniform(-0.04, 0.04)
            skin_t = 33.6 + random.uniform(-0.15, 0.15)
            resp = astro.baseline_resp + random.uniform(-0.5, 0.5)
            stress = 20.0 + random.uniform(-2, 3)
            sleep_q = 85.0
            activity = "REST"
            fluid_shift = astro.fluid_shift_score
            circadian_score = astro.circadian_disruption_score

            # Apply Scenario Drifts
            if active_sc == "eva_cardiac_stress":
                hr += 55.0 + random.uniform(-4, 6) # Up to 125-140 bpm
                hrv = max(14.0, hrv - 35.0)
                bp_sys += 28.0
                bp_dia += 14.0
                core_t += 0.85
                resp += 8.0
                stress = 78.0
                activity = "EVA"
            elif active_sc == "co2_spike" or active_sc == "co2_spike_crew":
                hr += 22.0
                spo2 = max(89.5, spo2 - 4.2)
                resp += 6.5
                stress += 35.0
                core_t += 0.3
            elif active_sc == "radiation_storm":
                astro.radiation_msv += 0.45 * self.speed # Rapid dose intake
                stress += 45.0
            elif active_sc == "sleep_deprivation":
                sleep_q = 34.0
                circadian_score = 72.0
                hrv = max(18.0, hrv - 28.0)
                stress = 82.0
                hr += 12.0
            elif active_sc == "dehydration":
                bp_sys -= 18.0
                bp_dia -= 10.0
                hr += 24.0
                skin_t -= 1.4
                fluid_shift = max(5.0, fluid_shift - 8.0)
            elif active_sc == "sensor_failure":
                if random.random() < 0.6:
                    spo2 = 0.0 # Sensor disconnect simulation
                    hr = 0.0

            # Clip values
            spo2 = min(100.0, max(0.0 if active_sc == "sensor_failure" else 70.0, spo2))
            hr = max(0.0 if active_sc == "sensor_failure" else 30.0, min(220.0, hr))

            vital_reading = VitalReading(
                astronaut_id=astro.id,
                timestamp=now,
                heart_rate=round(hr, 1),
                hrv=round(hrv, 1),
                spo2=round(spo2, 1),
                bp_systolic=round(bp_sys, 1),
                bp_diastolic=round(bp_dia, 1),
                core_temp=round(core_t, 2),
                skin_temp=round(skin_t, 2),
                respiratory_rate=round(resp, 1),
                sleep_quality=round(sleep_q, 1),
                stress_index=round(min(100.0, max(0.0, stress)), 1),
                activity_level=activity,
                fluid_shift_score=round(fluid_shift, 1),
                circadian_disruption_score=round(circadian_score, 1)
            )
            db.add(vital_reading)

            # Compute Composite Risk & Anomaly
            vitals_dict = {
                "heart_rate": hr, "hrv": hrv, "spo2": spo2,
                "bp_systolic": bp_sys, "bp_diastolic": bp_dia,
                "core_temp": core_t, "respiratory_rate": resp,
                "stress_index": stress, "sleep_quality": sleep_q,
                "circadian_disruption_score": circadian_score
            }
            baseline_dict = {
                "baseline_hr": astro.baseline_hr,
                "baseline_temp": astro.baseline_temp
            }
            env_dict = {
                "co2_ppm": env_reading.co2_ppm,
                "cabin_pressure_kpa": env_reading.cabin_pressure_kpa,
                "o2_pct": env_reading.o2_pct
            }

            risk_eval = analytics_engine.compute_composite_risk(vitals_dict, baseline_dict, env_dict)
            
            # Save Risk Snapshot
            factor_map = {f["name"]: f["score"] for f in risk_eval["factors"]}
            risk_snap = RiskSnapshot(
                astronaut_id=astro.id,
                timestamp=now,
                composite_risk=risk_eval["composite_risk_score"],
                factor_cardio=factor_map.get("Cardiovascular Autonomic Load", 0.0),
                factor_hypoxia=factor_map.get("Oxygen Saturation & Ventilation", 0.0),
                factor_thermal=factor_map.get("Thermoregulatory Core Stability", 0.0),
                factor_stress=factor_map.get("Stress & Circadian Rhythm Disruption", 0.0),
                factor_environment=factor_map.get("Spacecraft Environmental Strain", 0.0),
                explanation=risk_eval["summary_explanation"]
            )
            db.add(risk_snap)

            # Update Astronaut status
            new_status = "NOMINAL"
            if risk_eval["composite_risk_score"] >= 65.0 or active_sc:
                new_status = "CRITICAL" if risk_eval["composite_risk_score"] >= 75.0 else "WARNING"
            astro.status = new_status

            # Trigger Alerts if thresholds exceeded
            if active_sc == "eva_cardiac_stress" and hr > 120:
                active_alert = db.query(Alert).filter(
                    Alert.astronaut_id == astro.id, Alert.metric == "heart_rate", Alert.status == "ACTIVE"
                ).first()
                if not active_alert:
                    al = Alert(
                        astronaut_id=astro.id,
                        timestamp=now,
                        metric="heart_rate",
                        value=round(hr, 1),
                        threshold_level="CRITICAL" if hr > 135 else "WARNING",
                        message=f"High metabolic cardiac strain ({hr:.0f} bpm) detected during EVA maneuvers",
                        suggested_action="Recommend immediate tether pause, cooling garment pump rate increase, and metabolic assessment.",
                        status="ACTIVE"
                    )
                    db.add(al)
                    new_alerts.append(al)

            if spo2 < 93.0 and active_sc != "sensor_failure":
                active_alert = db.query(Alert).filter(
                    Alert.astronaut_id == astro.id, Alert.metric == "spo2", Alert.status == "ACTIVE"
                ).first()
                if not active_alert:
                    al = Alert(
                        astronaut_id=astro.id,
                        timestamp=now,
                        metric="spo2",
                        value=round(spo2, 1),
                        threshold_level="CRITICAL" if spo2 < 90.0 else "WARNING",
                        message=f"Acute desaturation event (SpO2: {spo2:.1f}%)",
                        suggested_action="Verify helmet/cabin O2 supply lines. Check for localized gas pocketing.",
                        status="ACTIVE"
                    )
                    db.add(al)
                    new_alerts.append(al)

            broadcast_vitals.append({
                "astronaut_id": astro.id,
                "name": astro.name,
                "callsign": astro.callsign,
                "status": astro.status,
                "vitals": vitals_dict,
                "risk": risk_eval,
                "radiation_msv": round(astro.radiation_msv, 2)
            })

        db.commit()

        # Build payload for WebSocket listeners
        payload = {
            "type": "TELEMETRY_UPDATE",
            "timestamp": now.isoformat(),
            "environment": {
                "co2_ppm": env_reading.co2_ppm,
                "o2_pct": env_reading.o2_pct,
                "cabin_temp_c": env_reading.cabin_temp_c,
                "humidity_pct": env_reading.humidity_pct,
                "cabin_pressure_kpa": env_reading.cabin_pressure_kpa,
                "noise_db": env_reading.noise_db
            },
            "crew": broadcast_vitals,
            "new_alerts_count": len(new_alerts),
            "active_scenarios": self.get_active_scenarios_list(),
            "simulation_speed": self.speed
        }

        # Notify all active WebSocket connections
        for listener in list(self.listeners):
            try:
                if asyncio.iscoroutinefunction(listener):
                    await listener(payload)
                else:
                    listener(payload)
            except Exception as e:
                pass

    async def run_loop(self):
        """Continuous background tick loop"""
        self.is_running = True
        print("Dr D Simulator background engine started.")
        while self.is_running:
            try:
                db = SessionLocal()
                try:
                    await self.step(db)
                finally:
                    db.close()
            except Exception as e:
                print(f"Simulator step error: {e}")

            # Sleep interval scaled by simulation speed
            base_sleep = 1.5 # 1.5 seconds per tick
            sleep_duration = max(0.05, base_sleep / self.speed)
            await asyncio.sleep(sleep_duration)

simulator = DrDSimulator()
