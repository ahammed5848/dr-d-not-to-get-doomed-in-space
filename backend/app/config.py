import os
import secrets
from typing import List
from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "Dr D"
    MISSION_NAME: str = "Dr D Ares-V"
    MISSION_DAY: int = 142
    MISSION_PHASE: str = "Mars Transit Phase II"
    TOTAL_MISSION_DAYS: int = 540
    COMM_DELAY_SECONDS: float = 4.2
    DISTANCE_FROM_EARTH_KM: float = 78450000.0

    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # Cryptographically secure key handling:
    # In production, require DR_D_SECRET_KEY or generate a high-entropy secret
    _env_secret: str = os.getenv("DR_D_SECRET_KEY") or os.getenv("SECRET_KEY") or ""
    if not _env_secret:
        if os.getenv("ENVIRONMENT", "development").lower() == "production":
            _env_secret = secrets.token_urlsafe(32)
        else:
            _env_secret = "dev-insecure-secret-key-replace-in-production-32chars"

    SECRET_KEY: str = _env_secret
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    DATABASE_URL: str = os.getenv("DR_D_DB_URL") or os.getenv("DATABASE_URL") or "sqlite:///./dr_d.db"

    # Explicit CORS configuration: Never allow wildcard '*' with credentials
    @property
    def CORS_ORIGINS(self) -> List[str]:
        env_origins = os.getenv("ALLOWED_ORIGINS") or os.getenv("CORS_ORIGINS")
        default_origins = [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:8000",
            "http://127.0.0.1:8000"
        ]
        if env_origins:
            custom = [o.strip() for o in env_origins.split(",") if o.strip()]
            combined = list(dict.fromkeys(default_origins + custom))
            return [o for o in combined if o != "*"]
        return default_origins

settings = Settings()
