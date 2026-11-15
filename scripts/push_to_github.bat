@echo off
set "PATH=C:\Users\AHAMMED\AppData\Local\Programs\Git\cmd;C:\Users\AHAMMED\AppData\Local\Programs\GitHubCLI;%PATH%"
cd /d "%~dp0.."
title Dr D - GitHub Publisher
cls
echo ========================================================
echo   DR D - GitHub Repository Publisher
echo   Target Repo: dr-d-not-to-get-doomed-in-space
echo ========================================================
echo.
echo [1/3] Checking GitHub CLI authentication...
gh auth status >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo Official GitHub browser authentication is required.
    echo Opening browser to log in securely...
    gh auth login --web --git-protocol https
)

echo.
echo [2/3] Verifying Git repository status...
git status

echo.
echo [3/3] Creating and pushing to repository 'dr-d-not-to-get-doomed-in-space'...
gh repo create dr-d-not-to-get-doomed-in-space --public --source=. --remote=origin --push
if %errorlevel% neq 0 (
    echo.
    echo If repository already exists remotely, pushing main branch directly...
    git branch -M main
    git push -u origin main
)

echo.
echo ========================================================
echo   Publication Complete!
echo ========================================================
echo Opening published repository in browser...
gh repo view --web
pause
