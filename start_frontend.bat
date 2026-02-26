@echo off
REM ============================================================================
REM FindMyPic - Start Frontend Only (Auto-opens browser)
REM ============================================================================

TITLE FindMyPic - Frontend
COLOR 0B

echo.
echo ============================================================================
echo                    FindMyPic - Starting Frontend
echo ============================================================================
echo.

REM Check if frontend is set up
if not exist "frontend\node_modules" (
    echo ❌ ERROR: Frontend not set up yet!
    echo.
    echo Please run SETUP.bat first.
    echo.
    pause
    exit /b 1
)

echo Starting frontend development server...
echo.
echo Frontend will be available at: http://localhost:5173
echo.
echo ⏳ Waiting for server to start, then opening browser...
echo.
echo Press Ctrl+C to stop the server.
echo.
echo ============================================================================
echo.

cd frontend

REM Start npm in background and capture the process
start /B npm run dev

REM Wait for frontend to be ready (max 30 seconds)
set ATTEMPTS=0
:wait_frontend
if %ATTEMPTS% GEQ 30 (
    echo.
    echo ⚠️  Frontend took longer than expected to start.
    echo Opening browser anyway...
    goto open_browser
)

REM Check if frontend is ready
curl -s -o nul -w "" --connect-timeout 1 http://127.0.0.1:5173/ >nul 2>&1
if errorlevel 1 (
    set /a ATTEMPTS+=1
    timeout /t 1 /nobreak >nul
    goto wait_frontend
)

:open_browser
echo.
echo ✅ Frontend ready! Opening browser...
echo.

REM Open browser
start "" http://localhost:5173

echo.
echo ============================================================================
echo Browser opened to http://localhost:5173
echo.
echo Keep this window open to keep the frontend running.
echo Press Ctrl+C to stop the server.
echo ============================================================================
echo.

REM Keep the window open
pause
