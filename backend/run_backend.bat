@echo off
title Dr D Backend API (Port 8000)
set "PATH=C:\Users\AHAMMED\AppData\Local\Programs\Python\Python313;C:\Users\AHAMMED\AppData\Local\Programs\Python\Python313\Scripts;%PATH%"
cd /d "%~dp0"
echo ========================================================
echo   DR D Backend API (Port 8000)
echo   FastAPI + Simulation Engine + WebSocket
echo   Docs: http://127.0.0.1:8000/docs
echo ========================================================
echo.
"C:\Users\AHAMMED\AppData\Local\Programs\Python\Python313\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause
