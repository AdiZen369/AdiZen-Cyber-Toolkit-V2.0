@echo off
title AdiZenWorks Web Interface
echo.
echo  =========================================
echo   AdiZenWorks Cybersecurity Toolkit V2.0
echo   Web Interface
echo  =========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.9+
    pause
    exit /b 1
)

echo [*] Checking dependencies...
pip install -r requirements.txt -q

cd /d "%~dp0"

echo [*] Starting Web Server at http://localhost:5000
echo [*] Press Ctrl+C to stop
python web\app.py

pause
