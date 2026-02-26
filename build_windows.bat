@echo off
REM FindMyPic - Windows Build Script
REM Creates a standalone executable with PyInstaller

echo ========================================
echo FindMyPic - Building for Windows
echo ========================================
echo.

REM Check if in correct directory
if not exist "backend" (
    echo ERROR: Please run this from the project root directory
    exit /b 1
)

REM Clean previous builds
echo [1/5] Cleaning previous builds...
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build
if exist "backend\dist" rmdir /s /q backend\dist
if exist "backend\build" rmdir /s /q backend\build

REM Build frontend
echo.
echo [2/5] Building frontend...
cd frontend
call npm run build
if errorlevel 1 (
    echo ERROR: Frontend build failed
    exit /b 1
)
cd ..

REM Install PyInstaller (if not already)
echo.
echo [3/5] Installing PyInstaller...
cd backend
call .venv\Scripts\python.exe -m pip install pyinstaller --quiet

REM Create PyInstaller spec file
echo.
echo [4/5] Creating executable...
echo # -*- mode: python ; coding: utf-8 -*- > FindMyPic.spec
echo. >> FindMyPic.spec
echo block_cipher = None >> FindMyPic.spec
echo. >> FindMyPic.spec
echo a = Analysis( >> FindMyPic.spec
echo     ['app/main.py'], >> FindMyPic.spec
echo     pathex=[], >> FindMyPic.spec
echo     binaries=[], >> FindMyPic.spec
echo     datas=[], >> FindMyPic.spec
echo     hiddenimports=['torch', 'transformers', 'chromadb', 'easyocr', 'facenet_pytorch'], >> FindMyPic.spec
echo     hookspath=[], >> FindMyPic.spec
echo     hooksconfig={}, >> FindMyPic.spec
echo     runtime_hooks=[], >> FindMyPic.spec
echo     excludes=[], >> FindMyPic.spec
echo     win_no_prefer_redirects=False, >> FindMyPic.spec
echo     win_private_assemblies=False, >> FindMyPic.spec
echo     cipher=block_cipher, >> FindMyPic.spec
echo     noarchive=False, >> FindMyPic.spec
echo ) >> FindMyPic.spec
echo. >> FindMyPic.spec
echo pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher) >> FindMyPic.spec
echo. >> FindMyPic.spec
echo exe = EXE( >> FindMyPic.spec
echo     pyz, >> FindMyPic.spec
echo     a.scripts, >> FindMyPic.spec
echo     a.binaries, >> FindMyPic.spec
echo     a.zipfiles, >> FindMyPic.spec
echo     a.datas, >> FindMyPic.spec
echo     [], >> FindMyPic.spec
echo     name='FindMyPic', >> FindMyPic.spec
echo     debug=False, >> FindMyPic.spec
echo     bootloader_ignore_signals=False, >> FindMyPic.spec
echo     strip=False, >> FindMyPic.spec
echo     upx=True, >> FindMyPic.spec
echo     upx_exclude=[], >> FindMyPic.spec
echo     runtime_tmpdir=None, >> FindMyPic.spec
echo     console=True, >> FindMyPic.spec
echo     disable_windowed_traceback=False, >> FindMyPic.spec
echo     argv_emulation=False, >> FindMyPic.spec
echo     target_arch=None, >> FindMyPic.spec
echo     codesign_identity=None, >> FindMyPic.spec
echo     entitlements_file=None, >> FindMyPic.spec
echo ) >> FindMyPic.spec

REM Build with PyInstaller
call .venv\Scripts\pyinstaller.exe FindMyPic.spec --clean

if errorlevel 1 (
    echo ERROR: PyInstaller build failed
    exit /b 1
)

REM Package everything
echo.
echo [5/5] Packaging application...
cd ..
if not exist "dist" mkdir dist
if not exist "dist\FindMyPic" mkdir dist\FindMyPic

copy backend\dist\FindMyPic.exe dist\FindMyPic\
xcopy frontend\dist dist\FindMyPic\frontend /E /I /Y
copy README.md dist\FindMyPic\
copy PRD.md dist\FindMyPic\

echo.
echo ========================================
echo ✅ BUILD COMPLETE!
echo ========================================
echo.
echo Application built in: dist\FindMyPic\
echo Executable: dist\FindMyPic\FindMyPic.exe
echo.
echo To test: cd dist\FindMyPic && FindMyPic.exe
echo.
echo Next steps:
echo  1. Test the executable on a clean Windows machine
echo  2. Create installer with Inno Setup (optional)
echo  3. Upload to GitHub Releases
echo.
pause
