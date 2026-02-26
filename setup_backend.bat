@echo off
REM ============================================================================
REM FindMyPic - Backend Setup
REM ============================================================================
REM This script sets up the Python backend and virtual environment
REM ============================================================================

TITLE FindMyPic - Backend Setup
COLOR 0B

echo.
echo ============================================================================
echo                    FindMyPic - Backend Setup
echo ============================================================================
echo.

REM ============================================================================
REM Step 1: Check Python
REM ============================================================================
echo [1/4] Checking Python installation...
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python not found!
    echo.
    echo Please install Python 3.10 or newer from:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANT: Check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo ✅ Python %PYVER% found
echo.

REM ============================================================================
REM Step 2: Detect GPU
REM ============================================================================
echo [2/4] Detecting GPU...
echo.

nvidia-smi --query-gpu=name --format=csv,noheader >nul 2>&1
if not errorlevel 1 (
    for /f "delims=" %%i in ('nvidia-smi --query-gpu=name --format=csv,noheader') do set GPU_NAME=%%i
    echo ✅ NVIDIA GPU detected: !GPU_NAME!
    echo.
    echo You have a GPU! Choose your version:
    echo.
    echo [G] GPU version - Fast, 8.6GB download (requires 4GB+ VRAM)
    echo [C] CPU version - Smaller, 500MB download (works anywhere)
    echo.
    echo ⚠️  NOTE: GPU version is 8GB download vs 500MB for CPU version
    echo.
    choice /C GC /M "Choose: [G]PU version (fast, 8GB) or [C]PU version (small, 500MB)"
    if errorlevel 2 (
        set INSTALL_TYPE=CPU
    ) else (
        set INSTALL_TYPE=GPU
    )
) else (
    echo ℹ️  No NVIDIA GPU detected
    echo.
    echo Installing CPU version:
    echo   • Works on any computer
    echo   • Small download (500MB)
    echo   • Good performance for up to 10,000 photos
    echo.
    set INSTALL_TYPE=CPU
)

echo.
echo 📦 Installing: %INSTALL_TYPE% version
echo.

REM ============================================================================
REM Step 3: Create Virtual Environment
REM ============================================================================
echo [3/4] Setting up Python environment...
echo.

cd backend

if exist ".venv" (
    echo ℹ️  Virtual environment already exists
    echo.
    choice /C YN /M "Reinstall dependencies"
    if errorlevel 2 (
        echo Skipping reinstall...
        cd ..
        goto :hardware_check
    )
    echo Removing old virtual environment...
    rmdir /s /q .venv
)

echo Creating virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)
echo ✅ Virtual environment created
echo.

REM ============================================================================
REM Step 4: Install Dependencies
REM ============================================================================
echo [4/4] Installing dependencies...
echo.
echo This will download and install Python packages.
echo Estimated time: 3-5 minutes
echo.

call .venv\Scripts\activate.bat

REM Upgrade pip first
echo Upgrading pip...
python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo ❌ Failed to upgrade pip
    pause
    exit /b 1
)

REM Install the right version based on GPU detection
if "%INSTALL_TYPE%"=="GPU" (
    echo.
    echo Installing GPU version (PyTorch with CUDA)...
    echo This is a large download (8.6GB) - please be patient...
    echo.
    pip install -r requirements.txt
) else (
    echo.
    echo Installing CPU version (smaller PyTorch)...
    echo.
    pip install -r requirements-runtime.txt
)

if errorlevel 1 (
    echo.
    echo ❌ Installation failed!
    echo.
    echo Common fixes:
    echo   1. Check your internet connection
    echo   2. Try running this script as Administrator
    echo   3. Delete backend\.venv folder and try again
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Backend dependencies installed successfully!
echo.

cd ..

:hardware_check
REM Continue to hardware check and model download
echo.
echo ============================================================================
echo Next: Running hardware detection and downloading AI models...
echo ============================================================================
echo.
pause

call setup_hardware.bat

exit /b 0
