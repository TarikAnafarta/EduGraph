@echo off
REM Quick start script for EduGraph API server (Windows)

echo ========================================
echo EduGraph API Server - Windows Launcher
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo.
echo Starting API server...
echo.
python run_api.py

pause
