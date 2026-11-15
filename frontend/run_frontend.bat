@echo off
title Dr D Frontend UI (Port 5173)
set "PATH=C:\Users\AHAMMED\AppData\Local\Programs\nodejs;%PATH%"
cd /d "%~dp0"
echo ========================================================
echo   DR D Mission Control UI (Port 5173)
echo   React 18 + Vite + Tailwind CSS
echo   URL: http://localhost:5173
echo ========================================================
echo.
call "C:\Users\AHAMMED\AppData\Local\Programs\nodejs\npm.cmd" run dev
pause
