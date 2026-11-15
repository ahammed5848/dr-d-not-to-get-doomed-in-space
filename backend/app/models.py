from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Index, Text
)
from sqlalchemy.orm import relationship
from .database import Base

def utc_now():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False, default="astronaut") # astronaut, surgeon, admin
    astronaut_id = Column(Integer, ForeignKey("astronauts.id"), nullable=True)

    astronaut = relationship("Astronaut", back_populates="user", uselist=False)

class Astronaut(Base):
    __tablename__ = "astronauts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    callsign = Column(String(50), nullable=False)
    role_title = Column(String(100), nullable=False) # e.g. Commander, Flight Engineer, Science Specialist, Medical Officer
    avatar_url = Column(String(255), nullable=True)
    age = Column(Integer, default=38)
    blood_type = Column(String(10), default="O+")
    status = Column(String(20), default="NOMINAL") # NOMINAL, WARNING, CRITICAL
    radiation_msv = Column(Float, default=142.5) # cumulative mSv
    radiation_limit_msv = Column(Float, default=600.0) # career/mission ceiling
    bone_density_loss_pct = Column(Float, default=2.4)
    muscle_mass_index = Column(Float, default=94.2)
    fluid_shift_score = Column(Float, default=18.0) # 0-100 ICP / facial edema risk
    circadian_disruption_score = Column(Float, default=14.0) # 0-100

    # Baseline vitals for anomaly detection
    baseline_hr = Column(Float, default=68.0)
    baseline_hrv = Column(Float, default=65.0)
    baseline_spo2 = Column(Float, default=98.5)
    baseline_bp_sys = Column(Float, default=118.0)
    baseline_bp_dia = Column(Float, default=76.0)
    baseline_temp = Column(Float, default=36.8)
    baseline_resp = Column(Float, default=14.0)

    user = relationship("User", back_populates="astronaut", uselist=False)
    vitals = relationship("VitalReading", back_populates="astronaut", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="astronaut", cascade="all, delete-orphan")
    checkins = relationship("DailyCheckin", back_populates="astronaut", cascade="all, delete-orphan")
    medical_notes = relationship("MedicalNote", back_populates="astronaut", cascade="all, delete-orphan")
    risk_snapshots = relationship("RiskSnapshot", back_populates="astronaut", cascade="all, delete-orphan")

class VitalReading(Base):
    __tablename__ = "vital_readings"

    id = Column(Integer, primary_key=True, index=True)
    astronaut_id = Column(Integer, ForeignKey("astronauts.id"), nullable=False, index=True)
    timestamp = Column(DateTime, default=utc_now, nullable=False, index=True)

    heart_rate = Column(Float, nullable=False) # bpm
    hrv = Column(Float, nullable=False) # ms (RMSSD)
    spo2 = Column(Float, nullable=False) # %
    bp_systolic = Column(Float, nullable=False) # mmHg
    bp_diastolic = Column(Float, nullable=False) # mmHg
    core_temp = Column(Float, nullable=False) # °C
    skin_temp = Column(Float, nullable=False) # °C
    respiratory_rate = Column(Float, nullable=False) # breaths/min
    sleep_quality = Column(Float, default=85.0) # 0-100
    stress_index = Column(Float, default=22.0) # 0-100
    activity_level = Column(String(30), default="REST") # REST, LIGHT, EXERCISE, EVA, SLEEP
    fluid_shift_score = Column(Float, default=18.0)
    circadian_disruption_score = Column(Float, default=14.0)

    astronaut = relationship("Astronaut", back_populates="vitals")

    __table_args__ = (
        Index("ix_vital_astronaut_timestamp", "astronaut_id", "timestamp"),
    )

class EnvironmentReading(Base):
    __tablename__ = "environment_readings"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=utc_now, nullable=False, index=True)
    co2_ppm = Column(Float, nullable=False, default=520.0)
    o2_pct = Column(Float, nullable=False, default=21.2)
    cabin_temp_c = Column(Float, nullable=False, default=22.4)
    humidity_pct = Column(Float, nullable=False, default=44.0)
    cabin_pressure_kpa = Column(Float, nullable=False, default=101.3)
    noise_db = Column(Float, nullable=False, default=58.2)

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    astronaut_id = Column(Integer, ForeignKey("astronauts.id"), nullable=True, index=True)
    timestamp = Column(DateTime, default=utc_now, nullable=False, index=True)
    metric = Column(String(50), nullable=False)
    value = Column(Float, nullable=False)
    threshold_level = Column(String(20), nullable=False) # WARNING, CRITICAL
    message = Column(String(255), nullable=False)
    suggested_action = Column(String(255), nullable=False)
    status = Column(String(20), default="ACTIVE", index=True) # ACTIVE, ACKNOWLEDGED, RESOLVED
    acknowledged_by = Column(String(100), nullable=True)
    acknowledged_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)

    astronaut = relationship("Astronaut", back_populates="alerts")

    __table_args__ = (
        Index("ix_alert_astronaut_timestamp", "astronaut_id", "timestamp"),
    )

class Threshold(Base):
    __tablename__ = "thresholds"

    id = Column(Integer, primary_key=True, index=True)
    metric = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    warning_low = Column(Float, nullable=True)
    warning_high = Column(Float, nullable=True)
    critical_low = Column(Float, nullable=True)
    critical_high = Column(Float, nullable=True)
    unit = Column(String(20), nullable=False)
    description = Column(String(255), nullable=True)

class DailyCheckin(Base):
    __tablename__ = "daily_checkins"

    id = Column(Integer, primary_key=True, index=True)
    astronaut_id = Column(Integer, ForeignKey("astronauts.id"), nullable=False, index=True)
    timestamp = Column(DateTime, default=utc_now, nullable=False, index=True)
    date = Column(String(20), nullable=False) # YYYY-MM-DD
    sleep_hours = Column(Float, nullable=False)
    sleep_quality_score = Column(Float, nullable=False) # 1-10
    physical_fatigue = Column(Float, nullable=False) # 1-10
    cognitive_fatigue = Column(Float, nullable=False) # 1-10
    mood_score = Column(Float, nullable=False) # 1-10
    muscle_soreness = Column(Float, nullable=False) # 1-10
    headache_score = Column(Float, nullable=False) # 1-10
    space_motion_sickness = Column(Float, nullable=False) # 1-10
    comments = Column(Text, nullable=True)

    astronaut = relationship("Astronaut", back_populates="checkins")

    __table_args__ = (
        Index("ix_checkin_astronaut_timestamp", "astronaut_id", "timestamp"),
    )

class MedicalNote(Base):
    __tablename__ = "medical_notes"

    id = Column(Integer, primary_key=True, index=True)
    astronaut_id = Column(Integer, ForeignKey("astronauts.id"), nullable=False, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    author_name = Column(String(100), nullable=False)
    timestamp = Column(DateTime, default=utc_now, nullable=False)
    category = Column(String(50), default="CLINICAL_OBSERVATION") # CLINICAL_OBSERVATION, COUNTERMEASURE, PHARMACOLOGY, PROTOCOL_UPDATE
    note_text = Column(Text, nullable=False)

    astronaut = relationship("Astronaut", back_populates="medical_notes")

class MissionInfo(Base):
    __tablename__ = "mission_info"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), default="Dr D Ares-V")
    current_day = Column(Integer, default=142)
    total_days = Column(Integer, default=540)
    phase = Column(String(100), default="Mars Transit Phase II")
    distance_from_earth_km = Column(Float, default=78450000.0)
    comm_delay_sec = Column(Float, default=4.2)
    eva_status = Column(String(50), default="STANDBY") # STANDBY, IN_PROGRESS, COMPLETED

class RiskSnapshot(Base):
    __tablename__ = "risk_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    astronaut_id = Column(Integer, ForeignKey("astronauts.id"), nullable=False, index=True)
    timestamp = Column(DateTime, default=utc_now, nullable=False, index=True)
    composite_risk = Column(Float, nullable=False) # 0-100
    factor_cardio = Column(Float, default=0.0)
    factor_hypoxia = Column(Float, default=0.0)
    factor_thermal = Column(Float, default=0.0)
    factor_stress = Column(Float, default=0.0)
    factor_environment = Column(Float, default=0.0)
    explanation = Column(String(255), nullable=True)

    astronaut = relationship("Astronaut", back_populates="risk_snapshots")

    __table_args__ = (
        Index("ix_risk_astronaut_timestamp", "astronaut_id", "timestamp"),
    )
