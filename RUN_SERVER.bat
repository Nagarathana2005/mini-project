@echo off
title HOSTEL MANAGEMENT SYSTEM - SERVER
echo ============================================================
echo          STARTING HOSTEL MANAGEMENT SYSTEM SERVER
echo ============================================================
echo.
cd /d "%~dp0"

echo [1/3] Checking and applying database migrations...
python manage.py makemigrations
python manage.py migrate
echo.

echo [2/3] Updating South Indian Mess Menu & Sample Data...
python manage.py seed_data
echo.

echo [3/3] Starting Django Server on http://127.0.0.1:8000/ ...
echo Keep this window open while using the website.
echo Press Ctrl+C in this window to stop the server anytime.
echo.
python manage.py runserver 127.0.0.1:8000
pause
