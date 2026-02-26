@echo off
REM ============================================================================
REM FindMyPic - Hardware Detection & Model Download
REM ============================================================================
REM This script:
REM   1. Detects your hardware (GPU, RAM, CPU)
REM   2. Selects optimal AI models for your hardware
REM   3. Downloads models (~540-850MB)
REM   4. Creates personalized config
REM ============================================================================

TITLE FindMyPic - Hardware Detection & Model Download
COLOR 0B

echo.
echo ============================================================================
echo           FindMyPic - Hardware Detection & Model Download
echo ============================================================================
echo.
echo This will:
echo   1. Detect your GPU, RAM, and CPU
echo   2. Select optimal AI models for your hardware
echo   3. Download models from official sources (~540-850MB)
echo   4. Cache models for offline use
echo.
echo Models are downloaded ONCE and cached in your user folder.
echo After this, FindMyPic works 100%% offline!
echo.
pause

REM ============================================================================
REM Check if backend is set up
REM ============================================================================
if not exist "backend\.venv\Scripts\python.exe" (
    echo.
    echo ❌ ERROR: Backend not set up yet!
    echo.
    echo Please run setup_backend.bat first.
    echo.
    pause
    exit /b 1
)

REM ============================================================================
REM Run hardware detection and model download
REM ============================================================================
echo.
echo Running hardware detection...
echo.

cd backend
call .venv\Scripts\activate.bat

python -c "from app.core.first_run import get_or_create_config; config = get_or_create_config(); print('\n✅ Hardware detection complete!'); print(f'\n📊 Your Configuration:'); print(f\"  • Model Tier: {config['optimizations']['model_tier']}\"); print(f\"  • CLIP Model: {config['optimizations']['clip_model']}\"); print(f\"  • Batch Size: {config['optimizations']['batch_size']}\"); print(f\"  • GPU Acceleration: {'Enabled' if config['optimizations']['use_gpu'] else 'Disabled'}\")"

if errorlevel 1 (
    echo.
    echo ❌ Hardware detection failed!
    echo.
    pause
    cd ..
    exit /b 1
)

cd ..

echo.
echo ============================================================================
echo Now downloading AI models...
echo ============================================================================
echo.
echo This will download:
echo   • CLIP model (image/text understanding) - ~300-600MB
echo   • FaceNet model (face recognition) - ~100MB
echo   • Text embedder (document search) - ~90MB
echo.
echo Total: ~540-850MB depending on your hardware
echo.
echo ⏳ This may take 5-10 minutes depending on your internet speed...
echo.
pause

REM Create and run model download script
cd backend
call .venv\Scripts\activate.bat

echo Downloading models...
python -c "print('\n🔄 Downloading CLIP model...\n'); from app.ai.clip_embed import CLIPEmbedder; embedder = CLIPEmbedder(); embedder.load_model(); print('\n✅ CLIP model downloaded and cached!\n')"

if errorlevel 1 (
    echo.
    echo ⚠️  CLIP model download failed or was interrupted.
    echo Models will download automatically when you first use the app.
    echo.
) else (
    echo ✅ CLIP model ready!
)

echo.
python -c "print('🔄 Downloading FaceNet model...\n'); from app.ai.face_embed import FaceEmbedder; embedder = FaceEmbedder(); embedder.load_model(); print('\n✅ FaceNet model downloaded and cached!\n')"

if errorlevel 1 (
    echo.
    echo ⚠️  FaceNet model download failed or was interrupted.
    echo Models will download automatically when you use face search.
    echo.
) else (
    echo ✅ FaceNet model ready!
)

echo.
python -c "print('🔄 Downloading Text Embedder model...\n'); from app.ai.text_embed import TextEmbedder; embedder = TextEmbedder(); embedder.load_model(); print('\n✅ Text Embedder downloaded and cached!\n')"

if errorlevel 1 (
    echo.
    echo ⚠️  Text Embedder download failed or was interrupted.
    echo Models will download automatically when you index documents.
    echo.
) else (
    echo ✅ Text Embedder ready!
)

cd ..

echo.
echo ============================================================================
echo ✅ Hardware Detection & Model Download Complete!
echo ============================================================================
echo.
echo Your AI models are now cached locally in:
echo   %USERPROFILE%\.cache\huggingface\
echo   %USERPROFILE%\.cache\torch\
echo.
echo FindMyPic is now ready to use 100%% offline!
echo.
echo ============================================================================
echo.

exit /b 0
