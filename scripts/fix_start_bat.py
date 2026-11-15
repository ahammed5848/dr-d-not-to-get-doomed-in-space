import os

batch_lines = [
    "@echo off",
    "setlocal",
    "",
    'set "PYTHON_EXE=C:\\Users\\AHAMMED\\AppData\\Local\\Programs\\Python\\Python313\\python.exe"',
    'set "NODE_DIR=C:\\Users\\AHAMMED\\AppData\\Local\\Programs\\nodejs"',
    'set "PATH=%NODE_DIR%;C:\\Users\\AHAMMED\\AppData\\Local\\Programs\\Python\\Python313;C:\\Users\\AHAMMED\\AppData\\Local\\Programs\\Python\\Python313\\Scripts;%PATH%"',
    "",
    "title DR D - Mission Control Launcher",
    "cls",
    "echo ========================================================",
    "echo   DR D - Astronaut Health Monitoring System",
    "echo   Your health guardian beyond Earth. - Ares-V Mission",
    "echo ========================================================",
    "echo.",
    "",
    'set "ROOT_DIR=%~dp0"',
    'set "BACKEND_DIR=%ROOT_DIR%backend"',
    'set "FRONTEND_DIR=%ROOT_DIR%frontend"',
    "",
    "echo [1/2] Launching Dr D Backend (FastAPI + Simulation Engine)...",
    'start "Dr D Backend API (Port 8000)" cmd /k "title Dr D Backend && cd /d %BACKEND_DIR% && ""%PYTHON_EXE%"" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"',
    "",
    "echo [2/2] Launching Dr D Frontend (React + Vite)...",
    'start "Dr D Frontend UI (Port 5173)" cmd /k "title Dr D Frontend && cd /d %FRONTEND_DIR% && set PATH=%NODE_DIR%;%%PATH%% && ""%NODE_DIR%\\npm.cmd"" run dev"',
    "",
    "echo.",
    "echo ========================================================",
    "echo   Mission Systems Launched Successfully!",
    "echo ========================================================",
    "echo.",
    "echo   Mission Control UI:  http://localhost:5173",
    "echo   REST API Docs:       http://localhost:8000/docs",
    "echo   Live WebSocket:      ws://localhost:8000/ws/live",
    "echo.",
    "echo Demo Credentials:",
    "echo   Flight Surgeon:      surgeon  / Password123!",
    "echo   Mission Commander:   schen    / Password123!",
    "echo   Flight Engineer:     erostova / Password123!",
    "echo   Mission Admin:       admin    / Password123!",
    "echo.",
    "echo Note: Keep the backend and frontend terminal windows open.",
    "echo ========================================================",
    "echo.",
    "pause",
    ""
]

content = "\r\n".join(batch_lines)

targets = [
    r"C:\Users\AHAMMED\.gemini\antigravity\scratch\dr_d_space_apps_final\dr_d_astronaut_health\start.bat",
    r"C:\Users\AHAMMED\.gemini\antigravity\scratch\hermes\start.bat"
]

for t in targets:
    with open(t, "wb") as f:
        f.write(content.encode("ascii"))
    print(f"Successfully wrote ASCII CRLF to {t}")
