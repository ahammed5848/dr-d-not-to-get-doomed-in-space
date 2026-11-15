import time
from collections import defaultdict
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserLogin, Token, UserResponse
from ..auth import verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

FAILED_ATTEMPTS = defaultdict(list)
MAX_FAILED_ATTEMPTS = 5
RATE_LIMIT_WINDOW = 60 # seconds

@router.post("/login", response_model=Token)
def login(login_data: UserLogin, request: Request, db: Session = Depends(get_db)):
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    
    # Clean old attempts and check rate limit
    recent_failures = [t for t in FAILED_ATTEMPTS[client_ip] if now - t < RATE_LIMIT_WINDOW]
    FAILED_ATTEMPTS[client_ip] = recent_failures
    if len(recent_failures) >= MAX_FAILED_ATTEMPTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded: Too many failed login attempts. Please wait 60 seconds before retrying."
        )

    user = db.query(User).filter(User.username == login_data.username).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        FAILED_ATTEMPTS[client_ip].append(now)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Clear failures on successful authentication
    FAILED_ATTEMPTS.pop(client_ip, None)
    
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role, "astronaut_id": user.astronaut_id}
    )
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)
