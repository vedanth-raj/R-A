@echo off
echo ============================================================
echo AI Research Agent - Ngrok Deployment
echo ============================================================
echo.

REM Check if ngrok exists
where ngrok >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Ngrok not found!
    echo.
    echo Please install ngrok:
    echo 1. Download from: https://ngrok.com/download
    echo 2. Extract ngrok.exe to this folder or add to PATH
    echo 3. Get auth token from: https://dashboard.ngrok.com/get-started/your-authtoken
    echo 4. Run: ngrok config add-authtoken YOUR_TOKEN
    echo.
    pause
    exit /b 1
)

echo [OK] Ngrok is installed
echo.
echo Starting Flask application on port 5000...
echo.

REM Start Flask in background
start "Flask App" cmd /k python web_app.py

REM Wait for Flask to start
timeout /t 5 /nobreak >nul

echo.
echo Starting ngrok tunnel...
echo Look for the "Forwarding" URL below - that's your public URL!
echo.
echo Press Ctrl+C to stop
echo.

REM Start ngrok
ngrok http 5000
