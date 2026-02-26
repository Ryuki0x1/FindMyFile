@echo off
REM ============================================================================
REM FindMyPic - One-Click Setup
REM ============================================================================
REM This script will:
REM   1. Detect your GPU (NVIDIA/AMD/Intel/None)
REM   2. Recommend CPU or GPU version
REM   3. Install Python dependencies automatically
REM   4. Download AI models on first run
REM   5. Launch the application
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
echo   [1] Detect your hardware (GPU detection)
echo   [2] Install the right version (CPU or GPU)
echo   [3] Download AI models (~750MB)
echo   [4] Launch FindMyPic
echo.
echo This will take 5-10 minutes depending on your internet speed.
echo.
pause

REM ============================================================================
REM Step 1: Check Python
REM ============================================================================
echo.
echo [1/5] Checking Python installation...
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python not found!
    echo.
    echo Please install Python 3.10 or newer from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Found Python %PYTHON_VERSION%

REM ============================================================================
REM Step 2: GPU Detection
REM ============================================================================
echo.
echo [2/5] Detecting your hardware...
echo.

REM Create temporary Python script for GPU detection
echo import sys > tmp_gpu_detect.py
echo try: >> tmp_gpu_detect.py
echo     import subprocess >> tmp_gpu_detect.py
echo     result = subprocess.run(['nvidia-smi'], capture_output=True, text=True) >> tmp_gpu_detect.py
echo     if result.returncode == 0: >> tmp_gpu_detect.py
echo         for line in result.stdout.split('\n'): >> tmp_gpu_detect.py
echo             if 'NVIDIA' in line and 'CUDA' in line: >> tmp_gpu_detect.py
echo                 print('GPU') >> tmp_gpu_detect.py
echo                 sys.exit(0) >> tmp_gpu_detect.py
echo     print('CPU') >> tmp_gpu_detect.py
echo except: >> tmp_gpu_detect.py
echo     print('CPU') >> tmp_gpu_detect.py

for /f "tokens=*" %%i in ('python tmp_gpu_detect.py') do set GPU_TYPE=%%i
del tmp_gpu_detect.py

if "%GPU_TYPE%"=="GPU" (
    echo ✅ NVIDIA GPU detected!
    echo.
    echo You have an NVIDIA graphics card. We recommend the GPU version for:
    echo   • 10x faster indexing
    echo   • Better performance with large photo collections
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
    echo ℹ️  No NVIDIA GPU detected (or nvidia-smi not found)
    echo.
    echo We'll install the CPU version:
    echo   • Works on any computer
    echo   • Small download (500MB)
    echo   • Good performance for up to 10,000 photos
    echo.
    set INSTALL_TYPE=CPU
)

echo.
echo 📦 Installing: %INSTALL_TYPE% version
echo.
pause

REM ============================================================================
REM Step 3: Create Virtual Environment
REM ============================================================================
echo.
echo [3/5] Setting up Python environment...
echo.

cd backend

if exist ".venv" (
    echo ℹ️  Virtual environment already exists, skipping...
) else (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
)

REM ============================================================================
REM Step 4: Install Dependencies
REM ============================================================================
echo.
echo [4/5] Installing dependencies...
echo.
echo This will download and install Python packages.
echo Estimated size: %INSTALL_TYPE% version
echo.

call .venv\Scripts\activate.bat

REM Upgrade pip first
echo Upgrading pip...
python -m pip install --upgrade pip --quiet

if "%INSTALL_TYPE%"=="CPU" (
    echo.
    echo Installing CPU-only version (500MB)...
    echo This uses CPU-only PyTorch to save space.
    echo.
    pip install -r requirements-runtime.txt
) else (
    echo.
    echo Installing GPU version (8GB)...
    echo This includes CUDA support for NVIDIA GPUs.
    echo.
    pip install -r requirements.txt
)

if errorlevel 1 (
    echo.
    echo ❌ Installation failed!
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

echo.
echo ✅ Dependencies installed successfully!

REM ============================================================================
REM Step 5: Install Frontend Dependencies
REM ============================================================================
echo.
echo [5/5] Setting up frontend...
echo.

cd ..\frontend

REM Check if Node.js is installed
where npm >nul 2>&1
if errorlevel 1 (
    echo.
    echo ⚠️  Node.js not found - Frontend features will be limited
    echo.
    echo To get the full experience, install Node.js from:
    echo https://nodejs.org/
    echo.
    echo You can continue without it, but you'll need to build the frontend later.
    echo.
    choice /C YN /M "Continue without Node.js"
    if errorlevel 2 exit /b 1
) else (
    if exist "node_modules" (
        echo ℹ️  Frontend dependencies already installed
    ) else (
        echo Installing frontend dependencies...
        call npm install
        if errorlevel 1 (
            echo ⚠️  Frontend installation failed, but backend will still work
        ) else (
            echo ✅ Frontend dependencies installed
        )
    )
)

cd ..

REM ============================================================================
REM Setup Complete!
REM ============================================================================
echo.
echo ============================================================================
echo                    ✅ Setup Complete!
echo ============================================================================
echo.
echo FindMyPic is now installed and ready to use!
echo.
echo 📋 What was installed:
echo   • Python dependencies (%INSTALL_TYPE% version)
echo   • Backend server (FastAPI)
if exist "frontend\node_modules" (
    echo   • Frontend UI (React)
)
echo.
echo 🚀 Next steps:
echo.
echo   1. Run: START.bat
echo   2. Wait for AI models to download (~750MB, first time only)
echo   3. Open browser to: http://localhost:5173
echo   4. Start indexing your photos!
echo.
echo 📁 AI models will be downloaded automatically on first use:
echo   • CLIP (image understanding) - ~600MB
echo   • FaceNet (face recognition) - ~100MB  
echo   • EasyOCR (text extraction) - ~50MB
echo.
echo These are downloaded once and cached for future use.
echo.
echo ============================================================================
echo.
pause

REM Ask if user wants to start now
echo.
choice /C YN /M "Would you like to start FindMyPic now"
if errorlevel 2 (
    echo.
    echo OK! Run START.bat whenever you're ready.
    echo.
    pause
    exit /b 0
)

REM Launch the application
echo.
echo Starting FindMyPic...
call START.bat
