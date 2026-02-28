@echo off
setlocal EnableDelayedExpansion
title FindMyPic Launcher
color 0B

echo.
echo  ========================================
echo    FindMyPic - Local AI Photo Search
echo    One-Click Launcher
echo  ========================================
echo.

:: Get the directory where this script lives
set "ROOT=%~dp0"

:: ----------------------------------------
:: Step 1: Pre-flight checks
:: ----------------------------------------
echo  [1/5] Running pre-flight checks...

:: Check Python venv exists
set "PYCHECK=!ROOT!backend\.venv\Scripts\python.exe"
if not exist "!PYCHECK!" (
    echo.
    echo  ❌ WARNING: Python virtual environment not found!
    echo.
    echo  The setup wizard ^(SETUP.bat^) will detect your GPU,
    echo  install the right version ^(CPU/GPU^), and download AI models.
    echo.
    echo.
    echo  Options:
    echo    [Y] Run SETUP.bat now ^(recommended^)
    echo    [N] Skip and continue anyway ^(if you set it up manually^)
    echo    [Q] Quit
    echo.
    choice /C YNQ /M "Choose"
    if errorlevel 3 (
        exit /b 1
    )
    if errorlevel 2 (
        echo.
        echo  ⚠️  Skipping setup check - proceeding anyway...
        echo.
        goto skip_venv_check
    )
    call SETUP.bat
    exit /b 0
)
:skip_venv_check

:: Check node_modules exists
set "NMCHECK=!ROOT!frontend\node_modules"
if not exist "!NMCHECK!" (
    echo.
    echo  ❌ WARNING: Frontend dependencies ^(node_modules^) not found!
    echo.
    echo  To install, run these commands in a terminal:
    echo      cd frontend
    echo      npm install
    echo.
    echo  Options:
    echo    [Y] Exit so you can install dependencies
    echo    [N] Skip and continue anyway ^(if you installed manually^)
    echo.
    choice /C YN /M "Choose"
    if errorlevel 2 (
        echo.
        echo  ⚠️  Skipping frontend check - proceeding anyway...
        echo.
        goto skip_frontend_check
    )
    exit /b 1
)
:skip_frontend_check

echo  [OK] Python venv found
echo  [OK] Frontend dependencies found
echo.

:: ----------------------------------------
:: Step 2: Check if backend is already running
:: ----------------------------------------
echo  [2/5] Checking backend (port 8000)...

curl -s -o nul -w "" --connect-timeout 2 http://127.0.0.1:8000/ >nul 2>&1
if !ERRORLEVEL! == 0 (
    echo  [OK] Backend is already running!
) else (
    echo  [..] Backend not running - starting it now...
    set "BDIR=!ROOT!backend"
    set "PY=!ROOT!backend\.venv\Scripts\python.exe"
    start "FindMyPic Backend" /min cmd /k "cd /d "!BDIR!" && "!PY!" -m app.main"
    echo  [OK] Backend starting in background...
)
echo.

:: ----------------------------------------
:: Step 3: Check if frontend is already running
:: ----------------------------------------
echo  [3/5] Checking frontend (port 5173)...

curl -s -o nul -w "" --connect-timeout 2 http://127.0.0.1:5173/ >nul 2>&1
if !ERRORLEVEL! == 0 (
    echo  [OK] Frontend is already running!
) else (
    echo  [..] Frontend not running - starting it now...
    set "FDIR=!ROOT!frontend"
    start "FindMyPic Frontend" /min cmd /k "cd /d "!FDIR!" && npm run dev"
    echo  [OK] Frontend starting in background...
)
echo.

:: ----------------------------------------
:: Step 4: Wait for both services to be ready
:: ----------------------------------------
echo  [4/5] Waiting for services to be ready...

:: Wait for backend (up to 180 seconds - first run downloads CLIP + FaceNet + EasyOCR)
echo        Waiting for backend...
echo.
echo        ℹ️  FIRST TIME? AI models (~750MB) will download automatically.
echo        This happens once and may take 5-10 minutes.
echo.
set "ATTEMPTS=0"
:wait_backend
if !ATTEMPTS! GEQ 180 (
    echo.
    echo  ERROR: Backend failed to start after 180 seconds.
    echo  Check the "FindMyPic Backend" window for errors.
    pause
    exit /b 1
)
curl -s -o nul -w "" --connect-timeout 2 http://127.0.0.1:8000/ >nul 2>&1
if !ERRORLEVEL! NEQ 0 (
    set /a ATTEMPTS+=1
    <nul set /p "=."
    timeout /t 1 /nobreak >nul
    goto wait_backend
)
echo.
echo  [OK] Backend ready at http://localhost:8000

:: Wait for frontend (up to 30 seconds)
echo        Waiting for frontend...
set "ATTEMPTS=0"
:wait_frontend
if !ATTEMPTS! GEQ 30 (
    echo.
    echo  ERROR: Frontend failed to start after 30 seconds.
    echo  Check the "FindMyPic Frontend" window for errors.
    pause
    exit /b 1
)
curl -s -o nul -w "" --connect-timeout 2 http://127.0.0.1:5173/ >nul 2>&1
if !ERRORLEVEL! NEQ 0 (
    set /a ATTEMPTS+=1
    <nul set /p "=."
    timeout /t 1 /nobreak >nul
    goto wait_frontend
)
echo.
echo  [OK] Frontend ready at http://localhost:5173
echo.

:: ----------------------------------------
:: Step 5: Open browser automatically
:: ----------------------------------------
echo  [5/5] Opening FindMyPic in your browser...
echo.

REM Add a small delay to ensure frontend is fully ready
timeout /t 2 /nobreak >nul

REM Open browser
start "" http://localhost:5173

echo.
echo  ========================================
echo    FindMyPic is running!
echo  ========================================
echo.
echo    🌐 Browser opened to: http://localhost:5173
echo.
echo    Frontend:  http://localhost:5173
echo    Backend:   http://localhost:8000
echo    API Docs:  http://localhost:8000/docs
echo.
echo    Backend and Frontend are running in
echo    separate minimized windows.
echo.
echo    To stop everything, close those
echo    windows or press Ctrl+C in each.
echo.
echo    This window can be closed safely.
echo  ========================================
echo.
echo  Press any key to close this launcher window...
pause >nul
