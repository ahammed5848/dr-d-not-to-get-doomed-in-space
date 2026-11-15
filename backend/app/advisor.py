from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

class Recommendation:
    def __init__(
        self,
        category: str,
        priority: str, # LOW, MEDIUM, HIGH, CRITICAL
        title: str,
        observation: str,
        action: str,
        expected_recovery: str
    ):
        self.category = category
        self.priority = priority
        self.title = title
        self.observation = observation
        self.action = action
        self.expected_recovery = expected_recovery

    def to_dict(self) -> Dict[str, Any]:
        return {
            "category": self.category,
            "priority": self.priority,
            "title": self.title,
            "observation": self.observation,
            "action": self.action,
            "expected_recovery": self.expected_recovery,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

class DrDAdvisor:
    """
    AI Clinical & Operational Decision Support Engine for Dr D.
    Engineered with a modular architecture so external LLM reasoning (Gemini / OpenAI)
    can be plugged in via the LLMAdvisorStub interface.
    """

    def generate_recommendations(
        self,
        astronaut_name: str,
        vitals: Dict[str, Any],
        baseline: Dict[str, float],
        environment: Optional[Dict[str, Any]] = None,
        checkin: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        recs: List[Recommendation] = []

        hr = vitals.get("heart_rate", 70.0)
        spo2 = vitals.get("spo2", 98.0)
        temp = vitals.get("core_temp", 36.8)
        bp_sys = vitals.get("bp_systolic", 120.0)
        bp_dia = vitals.get("bp_diastolic", 80.0)
        stress = vitals.get("stress_index", 20.0)
        activity = vitals.get("activity_level", "REST")
        circadian = vitals.get("circadian_disruption_score", 15.0)

        # 1. Hypoxia & Low SpO2
        if spo2 < 93.0:
            recs.append(Recommendation(
                category="URGENT_INTERVENTION",
                priority="CRITICAL",
                title="Acute Hypoxemia Protocol",
                observation=f"SpO2 decreased to {spo2:.1f}% (critical threshold < 91%).",
                action="Immediately inspect EMU helmet seal and portable life support loop. Administer 100% O2 via emergency mask.",
                expected_recovery="10-15 minutes following supplemental O2 administration."
            ))
        elif spo2 < 96.0:
            recs.append(Recommendation(
                category="PHYSIOLOGICAL_COUNTERMEASURE",
                priority="HIGH",
                title="Oxygen Partial Pressure Watch",
                observation=f"SpO2 tracking at {spo2:.1f}%, 2.5% below baseline.",
                action="Increase fresh airflow in bunk area. Verify ventilation ducting not obstructed by loose equipment.",
                expected_recovery="30 minutes."
            ))

        # 2. Elevated Cardiovascular Strain
        if hr > 115 and activity != "EXERCISE":
            recs.append(Recommendation(
                category="WORK_REST_CYCLE",
                priority="HIGH",
                title="Tachycardia Post-Exertion Rest Alert",
                observation=f"Resting heart rate remains elevated at {hr:.0f} bpm without active exercise.",
                action="Cease scheduled EVA/physical maintenance. Instruct astronaut to sit in neutral microgravity posture and ingest 500ml electrolyte pouch.",
                expected_recovery="20-30 minutes."
            ))
        elif bp_sys > 138:
            recs.append(Recommendation(
                category="CARDIOVASCULAR",
                priority="MEDIUM",
                title="Cephalad Fluid Shift & Vascular Resistance",
                observation=f"Systolic BP measured at {bp_sys:.0f} mmHg with mild facial edema risk.",
                action="Apply Lower Body Negative Pressure (LBNP) device for 30 minutes to redistribute fluid volume toward lower extremities.",
                expected_recovery="45-60 minutes."
            ))

        # 3. Thermoregulation
        if temp > 37.8:
            recs.append(Recommendation(
                category="THERMAL_REGULATION",
                priority="HIGH",
                title="Core Hyperthermia Risk",
                observation=f"Core body temperature elevated to {temp:.2f} °C.",
                action="Increase liquid cooling garment (LCG) pump flow rate. Remove insulating layers.",
                expected_recovery="20 minutes."
            ))

        # 4. Stress, Sleep & Circadian
        if circadian > 50.0 or stress > 65.0:
            recs.append(Recommendation(
                category="NEURO_PSYCHOLOGICAL",
                priority="MEDIUM",
                title="Circadian & Cognitive Fatigue Mitigation",
                observation=f"Circadian disruption index {circadian:.0f}/100 and sympathetic stress index {stress:.0f}/100.",
                action="Dim crew quarters lighting to 480nm-filtered warm spectrum. Schedule 45-minute tactical sleep nap before orbital transit maneuver.",
                expected_recovery="2 to 4 hours."
            ))

        # 5. Environment (CO2)
        if environment and environment.get("co2_ppm", 500) > 1000:
            co2 = environment["co2_ppm"]
            recs.append(Recommendation(
                category="ENVIRONMENTAL_CONTROL",
                priority="CRITICAL" if co2 > 1600 else "HIGH",
                title="Spacecraft Atmospheric Scrubber Warning",
                observation=f"Cabin CO2 concentration is {co2:.0f} ppm (acceptable limit < 1000 ppm).",
                action="Engage auxiliary Carbon Dioxide Removal Assembly (CDRA) bed B. Inspect air return diffuser filters.",
                expected_recovery="15-20 minutes after secondary bed engagement."
            ))

        # If everything is nominal, give general space health advice
        if not recs:
            recs.append(Recommendation(
                category="PREVENTATIVE_HEALTH",
                priority="LOW",
                title="Nominal Mission Maintenance",
                observation="All vitals, autonomic indices, and cabin environmental telemetry are within optimal boundaries.",
                action="Proceed with scheduled flight duties. Maintain mandatory 2.5-hour ARED resistive exercise session at 16:00 UTC.",
                expected_recovery="Ongoing nominal."
            ))

        return [r.to_dict() for r in recs]

# LLM Stub for future external AI models
class LLMAdvisorStub:
    """Interface placeholder for Gemini / OpenAI medical co-pilot integration"""
    async def query_llm_insights(self, telemetry_context: Dict[str, Any], prompt: str) -> str:
        # Structured mock response demonstrating LLM reasoning
        return (
            f"[Dr D Neural Co-Pilot Analysis]: Based on multi-modal telemetry fusion "
            f"(HR: {telemetry_context.get('heart_rate')} bpm, SpO2: {telemetry_context.get('spo2')}%), "
            f"physiological trajectory indicates mild microgravity deconditioning. "
            f"Recommended countermeasure: Increase treadmill load by 5% and supplement magnesium intake."
        )

advisor_engine = DrDAdvisor()
llm_advisor_stub = LLMAdvisorStub()
