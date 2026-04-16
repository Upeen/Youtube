@echo off
title YouTube Recommendation System

echo ============================================
echo   YouTube Recommendation System
echo ============================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

:: Install dependencies
echo Installing dependencies...
python -m pip install -r requirements.txt --quiet
echo.

:: Ask user what to do
echo Choose an option:
echo   1. Fetch data + Start dashboard
echo   2. Start dashboard only (use existing data)
echo.
set /p choice="Enter choice (1/2): "

if "%choice%"=="1" (
    echo.
    echo Fetching YouTube data...
    python fetch_data.py
    echo.
)

echo Starting Streamlit dashboard...
echo.
echo ============================================
echo   Dashboard will open in your browser
echo ============================================
echo.

python -m streamlit run app.py
pause