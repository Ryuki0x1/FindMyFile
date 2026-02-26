@echo off
REM ============================================================================
REM FindMyPic - Master Setup Script
REM ============================================================================
REM This orchestrates the complete setup process:
REM   1. Backend setup (Python dependencies)
REM   2. Hardware detection & model download
REM   3. Frontend setup (Node.js dependencies)
REM   4. Launch the application
REM ============================================================================

TITLE FindMyPic - Setup Wizard
COLOR 0B

echo.
echo ============================================================================
echo                        FindMyPic - Setup Wizard
echo ============================================================================
echo.
echo Welcome! This will set up FindMyPic on your computer.
echo.
echo What this does:
echo   [1] Setup Python backend
echo   [2] Detect hardware and download AI models (~540-850MB)
echo   [3] Setup React frontend
echo   [4] Launch FindMyPic
echo.
echo Estimated time: 10-15 minutes
echo.
pause

REM ============================================================================
REM Step 1: Backend Setup
REM ============================================================================
echo.
echo ============================================================================
echo STEP 1: Backend Setup
echo ============================================================================
echo.

call setup_backend.bat

if errorlevel 1 (
    echo.
    echo ❌ Backend setup failed!
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Backend setup complete!
echo.

REM ============================================================================
REM Step 2: Frontend Setup
REM ============================================================================
echo.
echo ============================================================================
echo STEP 2: Frontend Setup
echo ============================================================================
echo.

call setup_frontend.bat

if errorlevel 1 (
    echo.
    echo ❌ Frontend setup failed!
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Frontend setup complete!
echo.

REM ============================================================================
REM Setup Complete
REM ============================================================================
echo.
echo ============================================================================
echo                    ✅ Setup Complete!
echo ============================================================================
echo.
echo FindMyPic is ready to use!
echo.
echo Next steps:
echo   1. Run start.bat to launch the application
echo   2. Browser will open automatically to http://localhost:5173
echo   3. Start indexing your photos!
echo.
echo 📦 AI models have been downloaded and cached locally.
echo    FindMyPic now works 100%% offline!
echo.
echo ============================================================================
echo.

REM Ask if user wants to start now
choice /C YN /M "Would you like to start FindMyPic now"
if errorlevel 2 (
    echo.
    echo OK! Run start.bat whenever you're ready.
    echo.
    pause
    exit /b 0
)

REM Launch the application
echo.
echo Starting FindMyPic...
call start.bat

exit /b 0
