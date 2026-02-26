# FindMyPic - Deployment Guide

## 🎯 Problem: 8.6GB Package Size

The development environment includes full CUDA PyTorch (8GB), which is too large for distribution.

### Size Breakdown:
```
Development (.venv with CUDA):
├── torch (CUDA):      8.0 GB
├── scipy:             113 MB
├── opencv:            108 MB
├── other packages:    400 MB
└── TOTAL:            ~8.6 GB

Production (CPU-only):
├── torch (CPU):       200 MB  ← 40x smaller!
├── scipy:             113 MB
├── opencv:            108 MB
├── other packages:    100 MB
└── TOTAL:            ~500 MB  ← 94% reduction!
```

---

## 🚀 Solution: Multi-Strategy Deployment

### **Strategy 1: Separate Runtime Requirements** ✅ IMPLEMENTED
Use `requirements-runtime.txt` with CPU-only PyTorch for distribution.

**Files created:**
- `backend/requirements-runtime.txt` - Production deps (~500MB)
- `backend/requirements-dev.txt` - Development deps (includes testing tools)

### **Strategy 2: Models Downloaded on First Run**
Don't ship AI models with the app - download on first launch:
- CLIP model: ~600MB (auto-downloaded)
- FaceNet model: ~100MB (auto-downloaded)
- EasyOCR: ~50MB (auto-downloaded)

**Benefits:**
- Initial download: <100MB code only
- First run downloads models automatically
- Models cached in user's AppData folder

### **Strategy 3: PyInstaller Bundling**
Create a standalone executable with embedded Python.

### **Strategy 4: Electron Packaging** (Optional)
Package as desktop app with auto-updater.

---

## 📦 Deployment Options

### Option A: **CPU-Only Distribution** (Recommended for most users)
Best for users without NVIDIA GPUs or who want smaller download.

**Pros:**
- Small size (~500MB)
- Works on any computer
- Faster startup

**Cons:**
- Slower indexing (CPU vs GPU)
- Still very usable for <10,000 photos

**Build steps:**
```bash
# 1. Create clean environment
cd backend
python -m venv .venv-dist

# 2. Install CPU-only dependencies
.venv-dist\Scripts\activate
pip install -r requirements-runtime.txt

# 3. Test it works
python -m app.main
```

### Option B: **GPU-Enabled Distribution** (For power users)
For users with NVIDIA GPUs who want maximum speed.

**Pros:**
- 10x faster indexing
- Better for 50,000+ photos

**Cons:**
- 8.6GB download
- Requires NVIDIA GPU with CUDA

**Build steps:**
```bash
# Use existing requirements.txt (current setup)
pip install -r requirements.txt
```

### Option C: **ONNX Runtime** (Advanced - Future)
Convert models to ONNX format for maximum efficiency.

**Pros:**
- Smallest size (~300MB total)
- Fastest inference
- No PyTorch needed

**Cons:**
- Requires model conversion
- More complex setup

---

## 🔨 Build Scripts

### For Windows Executable (.exe)

**File: `build_windows.bat`**
```batch
@echo off
echo Building FindMyPic for Windows...

REM Clean previous builds
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

REM Install PyInstaller
pip install pyinstaller

REM Build backend
cd backend
pyinstaller --onefile ^
    --name FindMyPic ^
    --icon ../frontend/public/icon.ico ^
    --add-data "app;app" ^
    --hidden-import torch ^
    --hidden-import transformers ^
    --hidden-import chromadb ^
    app/main.py

cd ..
echo Build complete! Executable in backend/dist/FindMyPic.exe
```

### For Installer Package

**File: `build_installer.bat`**
```batch
@echo off
echo Creating FindMyPic installer...

REM Requires Inno Setup (free)
REM Download from: https://jrsoftware.org/isinfo.php

"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer_script.iss

echo Installer created: Output/FindMyPic_Setup.exe
```

---

## 📋 Deployment Checklist

### Pre-Build
- [ ] Update version in `backend/app/core/config.py`
- [ ] Test with `requirements-runtime.txt` (CPU-only)
- [ ] Run all tests: `pytest backend/tests/`
- [ ] Build frontend: `cd frontend && npm run build`
- [ ] Update CHANGELOG.md

### Build
- [ ] Create clean virtual environment
- [ ] Install runtime dependencies only
- [ ] Run PyInstaller build script
- [ ] Test executable on clean Windows machine
- [ ] Create installer with Inno Setup

### Post-Build
- [ ] Test installer on fresh Windows install
- [ ] Verify models download correctly on first run
- [ ] Check total installer size (<600MB)
- [ ] Upload to GitHub Releases
- [ ] Update README with download link

---

## 🎯 Recommended Approach

**For Initial Release:**
1. Use **Option A (CPU-only)** - smallest download
2. Include auto-detection: if CUDA available, suggest GPU version
3. Provide both versions on GitHub releases:
   - `FindMyPic_Setup_CPU.exe` (~500MB) - Recommended
   - `FindMyPic_Setup_GPU.exe` (~8GB) - For power users

**For Future:**
1. Implement ONNX conversion (Strategy 4)
2. Add cloud model hosting (download only needed models)
3. Progressive model loading (download OCR only if user uses it)

---

## 🔧 Testing Deployment Build

```bash
# 1. Test CPU-only build
cd backend
python -m venv .venv-test
.venv-test\Scripts\activate
pip install -r requirements-runtime.txt
python -m app.main

# 2. Test indexing works (should use CPU)
# Open browser: http://localhost:8000
# Index some test images

# 3. Verify package size
du -sh .venv-test  # Should be ~500MB
```

---

## 📊 Size Comparison

| Component | Development | Production | Savings |
|-----------|------------|------------|---------|
| PyTorch | 8.0 GB | 200 MB | **97.5%** |
| Dependencies | 600 MB | 300 MB | 50% |
| Total | 8.6 GB | 500 MB | **94%** |
| With models | 9.4 GB | 1.25 GB | **87%** |

---

## ❓ FAQ

**Q: Will CPU-only version work on my computer?**
A: Yes! It works on any Windows/Mac/Linux computer. GPU is optional.

**Q: How much slower is CPU vs GPU?**
A: About 5-10x slower for indexing. Search is instant on both.

**Q: Can users switch from CPU to GPU version later?**
A: Yes, just reinstall with GPU version. Database is compatible.

**Q: What about Mac M1/M2 chips?**
A: PyTorch has MPS (Metal) support for Apple Silicon. Add separate build.

---

## 🎬 Next Steps

1. ✅ Create `requirements-runtime.txt`
2. ⏳ Create `build_windows.bat` script
3. ⏳ Create `installer_script.iss` for Inno Setup
4. ⏳ Test on clean Windows VM
5. ⏳ Create GitHub release workflow
