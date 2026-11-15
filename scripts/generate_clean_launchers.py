import os

backend_bat = """@echo off
title Dr D Backend API (Port 8000)
set "PATH=C:\\Users\\AHAMMED\\AppData\\Local\\Programs\\Python\\Python313;C:\\Users\\AHAMMED\\AppData\\Local\\Programs\\Python\\Python313\\Scripts;%PATH%"
cd /d "%~dp0"
echo ========================================================
echo   DR D Backend API (Port 8000)
echo   FastAPI + Simulation Engine + WebSocket
echo   Docs: http://127.0.0.1:8000/docs
echo ========================================================
echo.
"C:\\Users\\AHAMMED\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause
"""

frontend_bat = """@echo off
title Dr D Frontend UI (Port 5173)
set "PATH=C:\\Users\\AHAMMED\\AppData\\Local\\Programs\\nodejs;%PATH%"
cd /d "%~dp0"
echo ========================================================
echo   DR D Mission Control UI (Port 5173)
echo   React 18 + Vite + Tailwind CSS
echo   URL: http://localhost:5173
echo ========================================================
echo.
call "C:\\Users\\AHAMMED\\AppData\\Local\\Programs\\nodejs\\npm.cmd" run dev
pause
"""

start_bat = """@echo off
title DR D - Mission Control Launcher
setlocal
cd /d "%~dp0"

echo ========================================================
echo   DR D - Astronaut Health Monitoring System
echo   Mission Control Launcher - Ares-V Mission
echo ========================================================
echo.
echo [1/2] Launching Dr D Backend on http://127.0.0.1:8000 ...
start "Dr D Backend" "%~dp0backend\\run_backend.bat"

echo [2/2] Launching Dr D Frontend on http://localhost:5173 ...
start "Dr D Frontend" "%~dp0frontend\\run_frontend.bat"

echo.
echo ========================================================
echo   Launch Sequence Completed!
echo ========================================================
echo.
echo   Mission Control UI:  http://localhost:5173
echo   REST API Docs:       http://localhost:8000/docs
echo   Live WebSocket:      ws://localhost:8000/ws/live
echo.
echo Demo Credentials:
echo   Flight Surgeon:      surgeon  / Password123!
echo   Mission Commander:   schen    / Password123!
echo   Flight Engineer:     erostova / Password123!
echo   Mission Admin:       admin    / Password123!
echo.
echo Keep both Backend and Frontend console windows open.
echo ========================================================
echo.
pause
"""

start_ps1 = """# DR D - Astronaut Health Monitoring System
# One-command startup script for PowerShell

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  DR D - Astronaut Health Monitoring System" -ForegroundColor Cyan
Write-Host "  Mission Control Launcher - Ares-V Transit" -ForegroundColor White
Write-Host "========================================================" -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendBat = Join-Path $scriptDir "backend\\run_backend.bat"
$frontendBat = Join-Path $scriptDir "frontend\\run_frontend.bat"

Write-Host "`n[1/2] Starting Dr D Backend (FastAPI on Port 8000)..." -ForegroundColor Yellow
Start-Process cmd -ArgumentList "/c `"$backendBat`""

Write-Host "[2/2] Starting Dr D Frontend (React Vite on Port 5173)..." -ForegroundColor Yellow
Start-Process cmd -ArgumentList "/c `"$frontendBat`""

Write-Host "`nDr D mission systems operational:" -ForegroundColor Green
Write-Host "  Mission Control UI:  http://localhost:5173" -ForegroundColor Cyan
Write-Host "  REST OpenAPI Docs:   http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "  Live Stream:         ws://localhost:8000/ws/live" -ForegroundColor Cyan
Write-Host "`nDemo Credentials:" -ForegroundColor White
Write-Host "  Flight Surgeon:      surgeon  / Password123!" -ForegroundColor White
Write-Host "  Commander Chen:      schen    / Password123!" -ForegroundColor White
Write-Host "  Flight Eng Elena:    erostova / Password123!" -ForegroundColor White
Write-Host "  Admin Director:      admin    / Password123!" -ForegroundColor White
Write-Host "========================================================`n" -ForegroundColor Cyan
"""

def to_crlf(text):
    return text.replace("\r\n", "\n").replace("\n", "\r\n").encode("ascii")

roots = [
    r"C:\Users\AHAMMED\.gemini\antigravity\scratch\dr_d_space_apps_final\dr_d_astronaut_health",
    r"C:\Users\AHAMMED\.gemini\antigravity\scratch\hermes"
]

for root in roots:
    with open(os.path.join(root, "backend", "run_backend.bat"), "wb") as f:
        f.write(to_crlf(backend_bat))
    with open(os.path.join(root, "frontend", "run_frontend.bat"), "wb") as f:
        f.write(to_crlf(frontend_bat))
    with open(os.path.join(root, "start.bat"), "wb") as f:
        f.write(to_crlf(start_bat))
    with open(os.path.join(root, "start.ps1"), "wb") as f:
        f.write(to_crlf(start_ps1))
    print(f"Generated clean scripts in {root}")
