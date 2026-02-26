@echo off
REM FindMyPic - CPU-Only Build (Small Size Distribution)
REM This creates a lightweight version without CUDA (500MB vs 8.6GB)

echo ========================================
echo FindMyPic - CPU-Only Build
echo ========================================
echo.
echo This will create a lightweight distribution
echo Size: ~500MB (vs 8.6GB with CUDA)
echo Works on: Any Windows PC
echo Performance: Good for up to 10,000 photos
echo.
pause

REM Check if in correct directory
if not exist "backend" (
    echo ERROR: Please run this from the project root directory
    exit /b 1
)

REM Create clean environment for distribution
echo.
echo [1/4] Creating clean Python environment...
cd backend
if exist ".venv-dist" rmdir /s /q .venv-dist
python -m venv .venv-dist

REM Install CPU-only dependencies
echo.
echo [2/4] Installing CPU-only dependencies...
echo This will download PyTorch CPU version (~200MB instead of 8GB)
call .venv-dist\Scripts\activate.bat
python -m pip install --upgrade pip --quiet
pip install -r requirements-runtime.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    exit /b 1
)

REM Test the installation
echo.
echo [3/4] Testing backend...
python -c "import torch; print('PyTorch CPU:', torch.__version__); print('CUDA available:', torch.cuda.is_available())"
python -c "from app.ai.clip_embed import CLIPEmbedder; print('CLIP embedder: OK')"
python -c "from app.ai.face_embed import FaceEmbedder; print('Face embedder: OK')"
python -c "from app.ai.ocr_engine import OCREngine; print('OCR engine: OK')"

if errorlevel 1 (
    echo ERROR: Backend test failed
    exit /b 1
)

REM Check size
echo.
echo [4/4] Checking package size...
for /f "tokens=3" %%a in ('dir .venv-dist /s /-c ^| findstr "bytes"') do set size=%%a
set /a size_mb=%size:~0,-9%
echo Total size: %size_mb% MB

cd ..

echo.
echo ========================================
echo ✅ CPU-ONLY BUILD COMPLETE!
echo ========================================
echo.
echo Environment: backend\.venv-dist
echo Size: ~500MB
echo.
echo To run with CPU-only build:
echo   1. cd backend
echo   2. .venv-dist\Scripts\activate
echo   3. python -m app.main
echo.
echo To create executable:
echo   Run: build_windows.bat
echo.
pause
