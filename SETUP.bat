@echo off
setlocal EnableDelayedExpansion
TITLE FindMyPic - Setup Wizard
COLOR 0B

echo.
echo ============================================================================
echo                        FindMyPic - Setup Wizard
echo ============================================================================
echo.
echo This will set up FindMyPic on your computer.
echo Estimated time: 10-15 minutes
echo.
pause

REM ============================================================================
REM Step 1: Check Prerequisites
REM ============================================================================
echo.
echo [1/4] Checking prerequisites...
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo.
    echo Install Python 3.10+ from https://python.org/downloads/
    echo IMPORTANT: Check "Add Python to PATH" during installation
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo ✅ Python %PYVER%

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found!
    echo.
    echo Install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('node --version 2^>^&1') do set NODEVER=%%i
echo ✅ Node.js %NODEVER%

REM Detect GPU
nvidia-smi --query-gpu=name --format=csv,noheader >nul 2>&1
if not errorlevel 1 (
    for /f "delims=" %%i in ('nvidia-smi --query-gpu=name --format=csv,noheader') do set GPU_NAME=%%i
    echo ✅ GPU detected: !GPU_NAME!
    echo.
    echo Choose version:
    echo   [G] GPU - Fast, 8.6GB download
    echo   [C] CPU - Small, 500MB download
    echo.
    choice /C GC /M "Choose"
    if errorlevel 2 (set INSTALL_TYPE=CPU) else (set INSTALL_TYPE=GPU)
) else (
    echo ℹ️  No GPU detected - Installing CPU version
    set INSTALL_TYPE=CPU
)

REM ============================================================================
REM Step 2: Backend Setup
REM ============================================================================
echo.
echo [2/4] Setting up backend...
echo.

cd backend

if exist ".venv" (
    echo Virtual environment exists
) else (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ❌ Failed to create venv
        pause
        exit /b 1
    )
)

call .venv\Scripts\activate.bat
python -m pip install --upgrade pip --quiet

if "%INSTALL_TYPE%"=="GPU" (
    echo Installing GPU version (8.6GB)...
    pip install -r requirements.txt --quiet
) else (
    echo Installing CPU version (500MB)...
    pip install -r requirements-runtime.txt --quiet
)

if errorlevel 1 (
    echo ❌ Installation failed
    pause
    exit /b 1
)

echo Installing document extraction libraries (PDF, DOCX, PPTX, XLSX)...
pip install PyMuPDF python-docx python-pptx openpyxl --quiet

if errorlevel 1 (
    echo ⚠️  Document libraries install failed - PDF/DOCX text extraction may not work
    echo     Try running manually: pip install PyMuPDF python-docx python-pptx openpyxl
) else (
    echo ✅ Document libraries ready
)

echo ✅ Backend ready

REM ============================================================================
REM Step 3: Download AI Models
REM ============================================================================
echo.
echo [3/4] Downloading AI models (~540-850MB)...
echo This happens once, then cached locally for offline use.
echo.

python -c "from app.core.first_run import get_or_create_config; get_or_create_config(); print('✅ Hardware detected')" 2>nul
python -c "from app.ai.clip_embed import CLIPEmbedder; e = CLIPEmbedder(); e.load_model(); print('✅ CLIP model ready')" 2>nul
python -c "from app.ai.face_embed import FaceEmbedder; e = FaceEmbedder(); e.load_model(); print('✅ FaceNet ready')" 2>nul
python -c "from app.ai.text_embed import TextEmbedder; e = TextEmbedder(); e.load_model(); print('✅ Text embedder ready')" 2>nul

cd ..

REM ============================================================================
REM Step 4: Frontend Setup
REM ============================================================================
echo.
echo [4/4] Setting up frontend...
echo.

cd frontend

if exist "node_modules" (
    echo npm packages already installed
) else (
    echo Installing npm packages...
    call npm install --silent
    if errorlevel 1 (
        echo ❌ npm install failed
        pause
        exit /b 1
    )
)

echo ✅ Frontend ready

cd ..

REM ============================================================================
REM Setup Complete
REM ============================================================================
echo.
echo ============================================================================
echo                    ✅ Setup Complete!
echo ============================================================================
echo.
echo FindMyPic is ready! AI models cached locally - now works 100%% offline.
echo.

choice /C YN /M "Start FindMyPic now"
if errorlevel 2 (
    echo.
    echo Run start.bat when ready!
    pause
    exit /b 0
)

echo.
call start.bat
exit /b 0
