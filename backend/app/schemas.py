from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

# Auth
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserResponse"

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    role: str
    astronaut_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

# Astronaut
class AstronautBase(BaseModel):
    name: str
    callsign: str
    role_title: str
    avatar_url: Optional[str] = None
    age: int = 38
    blood_type: str = "O+"
    status: str = "NOMINAL"
    radiation_msv: float = 142.5
    radiation_limit_msv: float = 600.0
    bone_density_loss_pct: float = 2.4
    muscle_mass_index: float = 94.2
    fluid_shift_score: float = 18.0
    circadian_disruption_score: float = 14.0

class AstronautResponse(AstronautBase):
    id: int
    baseline_hr: float
    baseline_hrv: float
    baseline_spo2: float
    baseline_bp_sys: float
    baseline_bp_dia: float
    baseline_temp: float
    baseline_resp: float
    latest_vitals: Optional[Dict[str, Any]] = None
    current_risk_score: Optional[float] = None
    active_alerts_count: int = 0

    model_config = ConfigDict(from_attributes=True)

# Vitals
class VitalReadingBase(BaseModel):
    heart_rate: float
    hrv: float
    spo2: float
    bp_systolic: float
    bp_diastolic: float
    core_temp: float
    skin_temp: float
    respiratory_rate: float
    sleep_quality: float = 85.0
    stress_index: float = 20.0
    activity_level: str = "REST"
    fluid_shift_score: float = 18.0
    circadian_disruption_score: float = 14.0

class VitalReadingCreate(VitalReadingBase):
    astronaut_id: int
    timestamp: Optional[datetime] = None

class VitalReadingResponse(VitalReadingBase):
    id: int
    astronaut_id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

# Environment
class EnvironmentReadingBase(BaseModel):
    co2_ppm: float
    o2_pct: float
    cabin_temp_c: float
    humidity_pct: float
    cabin_pressure_kpa: float
    noise_db: float

class EnvironmentReadingCreate(EnvironmentReadingBase):
    timestamp: Optional[datetime] = None

class EnvironmentReadingResponse(EnvironmentReadingBase):
    id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

# Alerts
class AlertBase(BaseModel):
    metric: str
    value: float
    threshold_level: str
    message: str
    suggested_action: str

class AlertCreate(AlertBase):
    astronaut_id: Optional[int] = None

class AlertUpdate(BaseModel):
    status: str # ACKNOWLEDGED or RESOLVED
    notes: Optional[str] = None

class AlertResponse(AlertBase):
    id: int
    astronaut_id: Optional[int] = None
    astronaut_name: Optional[str] = None
    astronaut_callsign: Optional[str] = None
    timestamp: datetime
    status: str
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None
    notes: Optional[str] = None
    research_context: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)

# Thresholds
class ThresholdBase(BaseModel):
    metric: str
    name: str
    warning_low: Optional[float] = None
    warning_high: Optional[float] = None
    critical_low: Optional[float] = None
    critical_high: Optional[float] = None
    unit: str
    description: Optional[str] = None

class ThresholdUpdate(BaseModel):
    warning_low: Optional[float] = None
    warning_high: Optional[float] = None
    critical_low: Optional[float] = None
    critical_high: Optional[float] = None

class ThresholdResponse(ThresholdBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# Daily Checkin
class DailyCheckinCreate(BaseModel):
    astronaut_id: int
    sleep_hours: float
    sleep_quality_score: float
    physical_fatigue: float
    cognitive_fatigue: float
    mood_score: float
    muscle_soreness: float
    headache_score: float
    space_motion_sickness: float
    comments: Optional[str] = None

class DailyCheckinResponse(DailyCheckinCreate):
    id: int
    timestamp: datetime
    date: str

    model_config = ConfigDict(from_attributes=True)

# Medical Notes
class MedicalNoteCreate(BaseModel):
    category: str = "CLINICAL_OBSERVATION"
    note_text: str

class MedicalNoteResponse(BaseModel):
    id: int
    astronaut_id: int
    author_id: int
    author_name: str
    timestamp: datetime
    category: str
    note_text: str

    model_config = ConfigDict(from_attributes=True)

# Risk Breakdown
class FactorScore(BaseModel):
    name: str
    score: float # 0-100
    impact: str # LOW, MEDIUM, HIGH, CRITICAL
    detail: str

class RiskAssessmentResponse(BaseModel):
    astronaut_id: int
    composite_risk_score: float # 0-100
    risk_level: str # NOMINAL, ELEVATED, HIGH, SEVERE
    factors: List[FactorScore]
    summary_explanation: str
    recommended_action: str

# Trend Forecast
class ForecastPoint(BaseModel):
    timestamp: str # ISO or relative minutes "+5m"
    predicted_value: float
    lower_bound: float
    upper_bound: float
    breach_warning: bool
    breach_critical: bool

class MetricForecast(BaseModel):
    metric: str
    current_value: float
    unit: str
    trend_direction: str # RISING, STABLE, FALLING
    points: List[ForecastPoint]
    warning_threshold: Optional[float] = None
    critical_threshold: Optional[float] = None

class ForecastResponse(BaseModel):
    astronaut_id: int
    generated_at: datetime
    forecast_minutes: int
    metrics: Dict[str, MetricForecast]

# Simulator
class ScenarioTriggerRequest(BaseModel):
    scenario_type: str # co2_spike, eva_cardiac_stress, radiation_storm, sleep_deprivation, dehydration, sensor_failure, nominal
    astronaut_id: Optional[int] = None # None means cabin/crew-wide or primary astronaut
    severity: Optional[str] = "moderate" # mild, moderate, severe

class SpeedChangeRequest(BaseModel):
    speed: int = Field(default=1, ge=1, le=100) # 1x, 10x, 60x

class MissionInfoResponse(BaseModel):
    name: str
    current_day: int
    total_days: int
    phase: str
    distance_from_earth_km: float
    comm_delay_sec: float
    eva_status: str
    active_scenarios: List[str]
    simulation_speed: int
