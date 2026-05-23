@echo off
title AdiZenWorks Cybersecurity Toolkit V2.0
echo.
echo  =========================================
echo   AdiZenWorks Cybersecurity Toolkit V2.0
echo  =========================================
echo.

:: Check Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.9+ from https://python.org
    pause
    exit /b 1
)

:: Install dependencies if needed
echo [*] Checking dependencies...
pip install -r requirements.txt -q

:: Set working directory to this script's folder
cd /d "%~dp0"

:: Run the desktop app
echo [*] Starting Desktop GUI...
python desktop\main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to start. Check the error above.
    pause
)
