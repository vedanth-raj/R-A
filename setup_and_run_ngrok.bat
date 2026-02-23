@echo off
echo ============================================================
echo LitWise AI - Ngrok Setup and Deployment
echo ============================================================
echo.

REM Check if ngrok.exe exists
if exist ngrok.exe (
    echo [OK] Ngrok found!
    goto :configure
)

echo [INFO] Downloading ngrok...
echo.

REM Download ngrok using PowerShell
powershell -Command "& {Invoke-WebRequest -Uri 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip' -OutFile 'ngrok.zip'}"

if exist ngrok.zip (
    echo [OK] Downloaded ngrok.zip
    echo [INFO] Extracting...
    powershell -Command "& {Expand-Archive -Path 'ngrok.zip' -DestinationPath '.' -Force}"
    del ngrok.zip
    echo [OK] Ngrok extracted!
) else (
    echo [ERROR] Failed to download ngrok
    echo Please download manually from: https://ngrok.com/download
    pause
    exit /b 1
)

:configure
echo.
echo [INFO] Configuring ngrok with your auth token...
ngrok config add-authtoken 34KcoJUaf3Jw6PEjxdgT8wnU3nL_39n8GEMK7YGtbq3FJdDDH

if %ERRORLEVEL% EQU 0 (
    echo [OK] Auth token configured!
) else (
    echo [WARNING] Failed to configure auth token
)

echo.
echo ============================================================
echo Starting Deployment
echo ============================================================
echo.
echo [1/2] Starting Flask application on port 5000...
echo.

REM Start Flask in a new window
start "LitWise AI - Flask" cmd /k "python web_app.py"

REM Wait for Flask to start
echo Waiting for Flask to initialize...
timeout /t 8 /nobreak >nul

echo.
echo [2/2] Starting ngrok tunnel...
echo.
echo ============================================================
echo YOUR PUBLIC URL WILL APPEAR BELOW
echo Look for the line starting with "Forwarding"
echo Example: https://abc123.ngrok.io
echo ============================================================
echo.

REM Start ngrok
ngrok http 5000
