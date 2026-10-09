@echo off
title GENERATE HOSTEL MANAGEMENT SYSTEM PPT
echo ============================================================
echo      GENERATING REVIEW 2 POWERPOINT PRESENTATION (.PPTX)
echo ============================================================
echo.
cd /d "%~dp0"
python create_ppt.py
echo.
echo ============================================================
echo Done! Your PowerPoint file is saved as:
echo Hostel_Management_System_Review2.pptx
echo ============================================================
echo.
pause
