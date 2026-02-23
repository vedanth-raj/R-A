@echo off
echo ============================================================
echo Restarting AI Research Agent
echo ============================================================
echo.

echo Stopping any running instances...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Flask App*" 2>nul
taskkill /F /IM ngrok.exe 2>nul

timeout /t 2 /nobreak >nul

echo.
echo Starting Flask application...
start "Flask App" cmd /k python web_app.py

timeout /t 8 /nobreak >nul

echo.
echo Starting Ngrok tunnel...
.\ngrok.exe http 5000

pause
