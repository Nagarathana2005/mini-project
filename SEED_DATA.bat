@echo off
title HOSTEL MANAGEMENT SYSTEM - POPULATE SAMPLE DATA
echo ============================================================
echo          POPULATING HOSTEL SYSTEM SAMPLE DATA
echo ============================================================
echo.
cd /d "%~dp0"
python manage.py seed_data
echo.
echo Completed!
pause
