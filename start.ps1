# DR D - Astronaut Health Monitoring System
# One-command startup script for PowerShell

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  DR D - Astronaut Health Monitoring System" -ForegroundColor Cyan
Write-Host "  Mission Control Launcher - Ares-V Transit" -ForegroundColor White
Write-Host "========================================================" -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendBat = Join-Path $scriptDir "backend\run_backend.bat"
$frontendBat = Join-Path $scriptDir "frontend\run_frontend.bat"

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
