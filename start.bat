@echo off
title DR D - Mission Control Launcher
setlocal
cd /d "%~dp0"

echo ========================================================
echo   DR D - Astronaut Health Monitoring System
echo   Mission Control Launcher - Ares-V Mission
echo ========================================================
echo.
echo [1/2] Launching Dr D Backend on http://127.0.0.1:8000 ...
start "Dr D Backend" "%~dp0backend\run_backend.bat"

echo [2/2] Launching Dr D Frontend on http://localhost:5173 ...
start "Dr D Frontend" "%~dp0frontend\run_frontend.bat"

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
