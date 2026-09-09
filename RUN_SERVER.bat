@echo off
title HOSTEL MANAGEMENT SYSTEM - SERVER
echo ============================================================
echo          STARTING HOSTEL MANAGEMENT SYSTEM SERVER
echo ============================================================
echo.
cd /d "%~dp0"

echo Applying any pending database migrations...
python manage.py migrate
echo.

echo Starting Django Server on http://127.0.0.1:8000/ ...
echo Press Ctrl+C in this window to stop the server anytime.
echo.
python manage.py runserver 127.0.0.1:8000
pause
