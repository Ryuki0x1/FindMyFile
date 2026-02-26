@echo off
REM ============================================================================
REM FindMyPic - Start Backend Only
REM ============================================================================

TITLE FindMyPic - Backend
COLOR 0B

echo.
echo ============================================================================
echo                    FindMyPic - Starting Backend
echo ============================================================================
echo.

REM Check if backend is set up
if not exist "backend\.venv\Scripts\python.exe" (
    echo ❌ ERROR: Backend not set up yet!
    echo.
    echo Please run SETUP.bat first.
    echo.
    pause
    exit /b 1
)

echo Starting backend server...
echo.
echo Backend will be available at: http://localhost:8000
echo API Documentation at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server.
echo.
echo ============================================================================
echo.

cd backend
call .venv\Scripts\activate.bat
python -m app.main

pause
