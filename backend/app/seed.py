from datetime import datetime, timezone, timedelta
import random
import math
from sqlalchemy.orm import Session
from .database import engine, Base, SessionLocal
from .models import (
    User, Astronaut, VitalReading, EnvironmentReading,
    Alert, Threshold, DailyCheckin, MedicalNote, MissionInfo, RiskSnapshot
)
from .auth import hash_password

def seed_database(db: Session):
    # Check if already seeded
    if db.query(User).first():
        return

    print("Seeding Dr D Database...")

    # 1. Mission Info
    mission = MissionInfo(
        name="Dr D Ares-V",
        current_day=142,
        total_days=540,
        phase="Mars Transit Phase II",
        distance_from_earth_km=78450000.0,
        comm_delay_sec=4.2,
        eva_status="STANDBY"
    )
    db.add(mission)

    # 2. Thresholds
    thresholds_data = [
        Threshold(metric="heart_rate", name="Heart Rate", warning_low=50.0, warning_high=100.0, critical_low=45.0, critical_high=125.0, unit="bpm", description="Normal resting heart rate in microgravity"),
        Threshold(metric="hrv", name="Heart Rate Variability", warning_low=35.0, warning_high=120.0, critical_low=20.0, critical_high=150.0, unit="ms", description="Autonomic nervous system recovery index (RMSSD)"),
        Threshold(metric="spo2", name="Blood Oxygen (SpO2)", warning_low=95.0, warning_high=100.0, critical_low=91.0, critical_high=100.0, unit="%", description="Peripheral capillary oxygen saturation"),
        Threshold(metric="bp_systolic", name="Systolic Blood Pressure", warning_low=95.0, warning_high=135.0, critical_low=85.0, critical_high=150.0, unit="mmHg", description="Upper blood pressure reading"),
        Threshold(metric="bp_diastolic", name="Diastolic Blood Pressure", warning_low=60.0, warning_high=90.0, critical_low=50.0, critical_high=100.0, unit="mmHg", description="Lower blood pressure reading"),
        Threshold(metric="core_temp", name="Core Body Temperature", warning_low=36.0, warning_high=37.8, critical_low=35.5, critical_high=38.6, unit="°C", description="Internal deep-body temperature"),
        Threshold(metric="skin_temp", name="Skin Surface Temperature", warning_low=32.0, warning_high=35.5, critical_low=30.0, critical_high=37.0, unit="°C", description="Perfusion and thermoregulation index"),
        Threshold(metric="respiratory_rate", name="Respiratory Rate", warning_low=10.0, warning_high=20.0, critical_low=8.0, critical_high=26.0, unit="breaths/min", description="Minute ventilation rate"),
        Threshold(metric="stress_index", name="Stress Index", warning_low=0.0, warning_high=65.0, critical_low=0.0, critical_high=85.0, unit="/100", description="Sympathetic tone and cognitive load score"),
        Threshold(metric="radiation_msv", name="Cumulative Radiation", warning_low=0.0, warning_high=350.0, critical_low=0.0, critical_high=500.0, unit="mSv", description="Cumulative cosmic ionizing dose"),
        Threshold(metric="co2_ppm", name="Cabin CO2 Concentration", warning_low=0.0, warning_high=1000.0, critical_low=0.0, critical_high=2500.0, unit="ppm", description="Atmospheric carbon dioxide in spacecraft"),
        Threshold(metric="o2_pct", name="Cabin O2 Percentage", warning_low=19.5, warning_high=23.5, critical_low=18.0, critical_high=25.0, unit="%", description="Atmospheric oxygen concentration"),
        Threshold(metric="cabin_pressure_kpa", name="Cabin Pressure", warning_low=95.0, warning_high=105.0, critical_low=90.0, critical_high=110.0, unit="kPa", description="Habitation module atmospheric pressure"),
        Threshold(metric="cabin_temp_c", name="Cabin Temperature", warning_low=18.0, warning_high=26.0, critical_low=15.0, critical_high=30.0, unit="°C", description="Ambient environmental temperature"),
    ]
    db.add_all(thresholds_data)
    db.commit()

    # 3. Astronauts
    astronauts_data = [
        Astronaut(
            name="Commander Sarah Chen",
            callsign="Valkyrie",
            role_title="Mission Commander & Pilot",
            avatar_url="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=200&auto=format&fit=crop&q=80",
            age=42,
            blood_type="A+",
            status="NOMINAL",
            radiation_msv=138.4,
            radiation_limit_msv=600.0,
            bone_density_loss_pct=2.1,
            muscle_mass_index=96.4,
            fluid_shift_score=16.0,
            circadian_disruption_score=12.0,
            baseline_hr=64.0,
            baseline_hrv=68.0,
            baseline_spo2=98.8,
            baseline_bp_sys=116.0,
            baseline_bp_dia=74.0,
            baseline_temp=36.7,
            baseline_resp=13.0,
        ),
        Astronaut(
            name="Dr. Marcus Vance",
            callsign="Geode",
            role_title="Chief Science Officer & Geologist",
            avatar_url="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=200&auto=format&fit=crop&q=80",
            age=39,
            blood_type="O+",
            status="NOMINAL",
            radiation_msv=145.2,
            radiation_limit_msv=600.0,
            bone_density_loss_pct=2.8,
            muscle_mass_index=92.1,
            fluid_shift_score=22.0,
            circadian_disruption_score=18.0,
            baseline_hr=70.0,
            baseline_hrv=62.0,
            baseline_spo2=98.2,
            baseline_bp_sys=120.0,
            baseline_bp_dia=78.0,
            baseline_temp=36.8,
            baseline_resp=14.0,
        ),
        Astronaut(
            name="Elena Rostova",
            callsign="Aegis",
            role_title="Flight Engineer & EVA Systems Lead",
            avatar_url="https://images.unsplash.com/photo-1580489944761-15a19d654956?w=200&auto=format&fit=crop&q=80",
            age=36,
            blood_type="B+",
            status="WARNING",
            radiation_msv=154.6,
            radiation_limit_msv=600.0,
            bone_density_loss_pct=3.2,
            muscle_mass_index=89.5,
            fluid_shift_score=29.0,
            circadian_disruption_score=34.0,
            baseline_hr=72.0,
            baseline_hrv=55.0,
            baseline_spo2=97.9,
            baseline_bp_sys=124.0,
            baseline_bp_dia=82.0,
            baseline_temp=37.1,
            baseline_resp=15.0,
        ),
        Astronaut(
            name="Dr. Alex Rivera",
            callsign="Orion",
            role_title="Medical Specialist & Life Support Lead",
            avatar_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&auto=format&fit=crop&q=80",
            age=34,
            blood_type="AB-",
            status="NOMINAL",
            radiation_msv=132.8,
            radiation_limit_msv=600.0,
            bone_density_loss_pct=1.8,
            muscle_mass_index=97.0,
            fluid_shift_score=14.0,
            circadian_disruption_score=10.0,
            baseline_hr=62.0,
            baseline_hrv=72.0,
            baseline_spo2=99.1,
            baseline_bp_sys=114.0,
            baseline_bp_dia=72.0,
            baseline_temp=36.6,
            baseline_resp=12.0,
        ),
    ]
    db.add_all(astronauts_data)
    db.commit()

    # 4. Users (4 astronauts, 1 surgeon, 1 admin)
    users_data = [
        User(username="schen", hashed_password=hash_password("Password123!"), full_name="Sarah Chen", role="astronaut", astronaut_id=1),
        User(username="mvance", hashed_password=hash_password("Password123!"), full_name="Marcus Vance", role="astronaut", astronaut_id=2),
        User(username="erostova", hashed_password=hash_password("Password123!"), full_name="Elena Rostova", role="astronaut", astronaut_id=3),
        User(username="arivera", hashed_password=hash_password("Password123!"), full_name="Alex Rivera", role="astronaut", astronaut_id=4),
        User(username="surgeon", hashed_password=hash_password("Password123!"), full_name="Dr. Evelyn Reed (Flight Surgeon)", role="surgeon", astronaut_id=None),
        User(username="admin", hashed_password=hash_password("Password123!"), full_name="Director Robert Torres", role="admin", astronaut_id=None),
    ]
    db.add_all(users_data)
    db.commit()

    # 5. Seed historical readings (past 2 hours, 1 reading every 2 minutes for charts)
    now = datetime.now(timezone.utc)
    past_points = 60 # 60 points = 2 hours of data
    
    for i in range(past_points, 0, -1):
        t = now - timedelta(minutes=i * 2)
        # Environment
        env = EnvironmentReading(
            timestamp=t,
            co2_ppm=520.0 + 30.0 * math.sin(i / 10.0) + random.uniform(-10, 10),
            o2_pct=21.2 + 0.2 * math.sin(i / 15.0) + random.uniform(-0.05, 0.05),
            cabin_temp_c=22.3 + 0.4 * math.cos(i / 8.0) + random.uniform(-0.1, 0.1),
            humidity_pct=43.5 + 1.5 * math.sin(i / 12.0) + random.uniform(-0.5, 0.5),
            cabin_pressure_kpa=101.3 + random.uniform(-0.2, 0.2),
            noise_db=58.0 + random.uniform(-1.5, 2.5)
        )
        db.add(env)

        # Astronaut Vitals
        for astro in astronauts_data:
            # Add some variability per astronaut
            is_warning_astro = (astro.id == 3 and i < 20)
            hr_drift = 16.0 if is_warning_astro else 0.0
            stress_drift = 25.0 if is_warning_astro else 0.0
            spo2_drift = -2.2 if is_warning_astro else 0.0

            vital = VitalReading(
                astronaut_id=astro.id,
                timestamp=t,
                heart_rate=round(astro.baseline_hr + hr_drift + 4.0 * math.sin(i / 5.0) + random.uniform(-2, 2), 1),
                hrv=round(astro.baseline_hrv - (stress_drift * 0.4) + random.uniform(-3, 3), 1),
                spo2=round(min(100.0, astro.baseline_spo2 + spo2_drift + random.uniform(-0.3, 0.3)), 1),
                bp_systolic=round(astro.baseline_bp_sys + (stress_drift * 0.3) + random.uniform(-2, 2), 1),
                bp_diastolic=round(astro.baseline_bp_dia + (stress_drift * 0.2) + random.uniform(-1.5, 1.5), 1),
                core_temp=round(astro.baseline_temp + (0.3 if is_warning_astro else 0.0) + random.uniform(-0.08, 0.08), 2),
                skin_temp=round(33.6 + random.uniform(-0.2, 0.2), 2),
                respiratory_rate=round(astro.baseline_resp + (3.0 if is_warning_astro else 0.0) + random.uniform(-0.8, 0.8), 1),
                sleep_quality=82.0 if astro.id != 3 else 64.0,
                stress_index=round(min(100.0, 22.0 + stress_drift + random.uniform(-3, 3)), 1),
                activity_level="EXERCISE" if (i % 25 < 4) else "REST",
                fluid_shift_score=round(astro.fluid_shift_score + random.uniform(-0.5, 0.5), 1),
                circadian_disruption_score=round(astro.circadian_disruption_score + random.uniform(-0.5, 0.5), 1)
            )
            db.add(vital)

    # 6. Seed Alerts
    alerts_data = [
        Alert(
            astronaut_id=3,
            timestamp=now - timedelta(minutes=18),
            metric="heart_rate",
            value=106.4,
            threshold_level="WARNING",
            message="Sustained elevated heart rate (106 bpm) post-cycle ergometer session",
            suggested_action="Recommend 20-minute rest in quarters and active electrolyte rehydration.",
            status="ACTIVE"
        ),
        Alert(
            astronaut_id=3,
            timestamp=now - timedelta(minutes=45),
            metric="sleep_quality",
            value=58.0,
            threshold_level="WARNING",
            message="Circadian rhythm disruption detected: sleep latency exceeded 75 min",
            suggested_action="Adjust blue-light spectrum in bunk; consider 0.5mg melatonin protocol.",
            status="ACKNOWLEDGED",
            acknowledged_by="Dr. Evelyn Reed (Flight Surgeon)",
            acknowledged_at=now - timedelta(minutes=30),
            notes="Noted during flight surgeon handover. Astronaut will be prompted to begin wind-down at 21:00 UTC."
        ),
        Alert(
            astronaut_id=2,
            timestamp=now - timedelta(hours=3),
            metric="co2_ppm",
            value=940.0,
            threshold_level="WARNING",
            message="Cabin CO2 near warning threshold during dual-crew exercise protocol",
            suggested_action="Activate auxiliary ventilation loop in Module Bravo.",
            status="RESOLVED",
            acknowledged_by="Director Robert Torres",
            acknowledged_at=now - timedelta(hours=2, minutes=40),
            notes="Aux scrubber loop B engaged. CO2 stabilized at 520 ppm."
        )
    ]
    db.add_all(alerts_data)

    # 7. Seed Daily Checkins
    for astro in astronauts_data:
        checkin = DailyCheckin(
            astronaut_id=astro.id,
            timestamp=now - timedelta(hours=8),
            date=(now - timedelta(days=1)).strftime("%Y-%m-%d"),
            sleep_hours=7.2 if astro.id != 3 else 5.4,
            sleep_quality_score=8.5 if astro.id != 3 else 6.0,
            physical_fatigue=2.5 if astro.id != 3 else 5.8,
            cognitive_fatigue=2.0 if astro.id != 3 else 4.5,
            mood_score=9.0 if astro.id != 3 else 6.8,
            muscle_soreness=3.0 if astro.id != 3 else 6.0,
            headache_score=1.0 if astro.id != 3 else 4.0,
            space_motion_sickness=1.0,
            comments="Nominal day during morning systems check." if astro.id != 3 else "Mild frontal headache during midday workout, resolved after fluid intake."
        )
        db.add(checkin)

    # 8. Seed Medical Notes
    notes_data = [
        MedicalNote(
            astronaut_id=3,
            author_id=5,
            author_name="Dr. Evelyn Reed (Flight Surgeon)",
            timestamp=now - timedelta(hours=5),
            category="CLINICAL_OBSERVATION",
            note_text="Elena has logged slightly reduced sleep quality over consecutive sol cycles. Fluid shift score remains moderate (29/100) with slight cephalad redistribution typical of mission day 140+. Monitoring cardiovascular recovery."
        ),
        MedicalNote(
            astronaut_id=1,
            author_id=5,
            author_name="Dr. Evelyn Reed (Flight Surgeon)",
            timestamp=now - timedelta(days=1),
            category="COUNTERMEASURE",
            note_text="Commander Chen completed high-resistance ARED protocol with 100% adherence. Bone density and muscular indexes tracking above 95% of pre-flight baseline."
        )
    ]
    db.add_all(notes_data)

    db.commit()
    print("Dr D database seeded successfully!")

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
