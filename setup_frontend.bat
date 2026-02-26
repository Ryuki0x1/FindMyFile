@echo off
REM ============================================================================
REM FindMyPic - Frontend Setup
REM ============================================================================
REM This script sets up the React frontend and Node.js dependencies
REM ============================================================================

TITLE FindMyPic - Frontend Setup
COLOR 0B

echo.
echo ============================================================================
echo                    FindMyPic - Frontend Setup
echo ============================================================================
echo.

REM ============================================================================
REM Step 1: Check Node.js
REM ============================================================================
echo [1/2] Checking Node.js installation...
echo.

node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Node.js not found!
    echo.
    echo Please install Node.js 18 or newer from:
    echo https://nodejs.org/
    echo.
    echo Download the LTS (Long Term Support) version.
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('node --version 2^>^&1') do set NODEVER=%%i
echo ✅ Node.js %NODEVER% found
echo.

REM ============================================================================
REM Step 2: Install Frontend Dependencies
REM ============================================================================
echo [2/2] Installing frontend dependencies...
echo.

cd frontend

if exist "node_modules" (
    echo ℹ️  node_modules already exists
    echo.
    choice /C YN /M "Reinstall dependencies"
    if errorlevel 2 (
        echo Skipping reinstall...
        cd ..
        goto :done
    )
    echo Removing old node_modules...
    rmdir /s /q node_modules
)

echo.
echo Installing npm packages...
echo This will take 2-3 minutes...
echo.

call npm install

if errorlevel 1 (
    echo.
    echo ❌ Installation failed!
    echo.
    echo Common fixes:
    echo   1. Check your internet connection
    echo   2. Delete frontend\node_modules and try again
    echo   3. Run: npm cache clean --force
    echo.
    pause
    cd ..
    exit /b 1
)

echo.
echo ✅ Frontend dependencies installed successfully!
echo.

cd ..

:done
echo.
echo ============================================================================
echo ✅ Frontend Setup Complete!
echo ============================================================================
echo.

exit /b 0
