# Batch Files Guide

This document explains all the batch files in FindMyPic and when to use them.

## 🚀 Setup Scripts

### `SETUP.bat` - Master Setup (Use this first!)
**Purpose:** Complete one-click setup for first-time installation.

**What it does:**
1. Runs `setup_backend.bat` - Installs Python dependencies (does NOT call hardware setup)
2. Runs `setup_hardware.bat` - Detects hardware and downloads AI models
3. Runs `setup_frontend.bat` - Installs Node.js dependencies
4. Offers to launch the application

**Workflow Order:**
```
SETUP.bat
├─→ 1. setup_backend.bat (Python + venv + dependencies)
├─→ 2. setup_hardware.bat (GPU detection + model download)
├─→ 3. setup_frontend.bat (Node.js + npm packages)
└─→ 4. Offer to run start.bat
```

**When to use:**
- First time installing FindMyPic
- After cloning from GitHub
- To reinstall everything from scratch

**Command:**
```batch
SETUP.bat
```

---

### `setup_backend.bat` - Backend Setup
**Purpose:** Setup Python backend and dependencies.

**What it does:**
1. Checks Python installation
2. Detects GPU and asks CPU vs GPU version
3. Creates Python virtual environment
4. Installs Python packages (PyTorch, FastAPI, etc.)

**Note:** This script does NOT call `setup_hardware.bat`. The master `SETUP.bat` calls it separately for cleaner workflow.

**When to use:**
- Standalone backend setup
- Updating Python dependencies
- Switching between CPU/GPU versions

**Command:**
```batch
setup_backend.bat
```

---

### `setup_hardware.bat` - Hardware Detection & Model Download
**Purpose:** Detect hardware and download optimal AI models.

**What it does:**
1. Detects GPU, RAM, and CPU
2. Creates personalized config (`data/config.json`)
3. Downloads CLIP model (~300-600MB based on hardware)
4. Downloads FaceNet model (~100MB)
5. Downloads Text Embedder model (~90MB)
6. Caches models in `~/.cache/` for offline use

**When to use:**
- Called automatically by `SETUP.bat` after backend setup
- To re-download models
- If models are corrupted or deleted
- To detect new GPU after hardware upgrade

**Command:**
```batch
setup_hardware.bat
```

**Note:** This requires backend to be set up first (needs Python venv in `backend/.venv/`).

---

### `setup_frontend.bat` - Frontend Setup
**Purpose:** Setup React frontend and Node.js dependencies.

**What it does:**
1. Checks Node.js installation
2. Installs npm packages (React, Vite, TypeScript, etc.)

**When to use:**
- Standalone frontend setup
- Updating frontend dependencies
- If `node_modules` gets corrupted

**Command:**
```batch
setup_frontend.bat
```

---

## ▶️ Start Scripts

### `start.bat` - Full Application Launcher (Use this to run!)
**Purpose:** Start both backend and frontend with one click.

**What it does:**
1. Checks if setup is complete
2. Starts backend server (port 8000) in background
3. Starts frontend dev server (port 5173) in background
4. Waits for both to be ready
5. **Automatically opens browser to http://localhost:5173**

**When to use:**
- Every time you want to use FindMyPic
- After running SETUP.bat

**Command:**
```batch
start.bat
```

**Features:**
- ✅ Auto-detects if services are already running
- ✅ Auto-opens browser when ready
- ✅ Runs services in minimized windows
- ✅ Shows clear status messages

---

### `start_backend.bat` - Backend Only
**Purpose:** Start only the backend API server.

**What it does:**
- Starts FastAPI server on port 8000
- Shows API documentation URL

**When to use:**
- Testing backend separately
- Backend development
- Using API without frontend

**Command:**
```batch
start_backend.bat
```

**URLs:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

---

### `start_frontend.bat` - Frontend Only (Auto-opens browser)
**Purpose:** Start only the frontend development server.

**What it does:**
- Starts Vite dev server on port 5173
- Waits for server to be ready
- **Automatically opens browser**

**When to use:**
- Frontend development (with backend running separately)
- Testing frontend changes

**Command:**
```batch
start_frontend.bat
```

**Features:**
- ✅ Auto-opens browser when ready
- ✅ Waits up to 30 seconds for server

---

## 🔧 Build Scripts

### `build_windows.bat`
**Purpose:** Build production release for Windows (GPU version).

**When to use:**
- Creating distributable .exe
- Production deployment

---

### `build_cpu_only.bat`
**Purpose:** Build production release for Windows (CPU version).

**When to use:**
- Creating smaller distributable
- For computers without GPU

---

## 📋 Quick Reference

### First Time Setup
```batch
# 1. Run complete setup (this runs everything in order)
SETUP.bat
# Runs: setup_backend.bat → setup_hardware.bat → setup_frontend.bat

# 2. Start the application (browser opens automatically)
start.bat
```

### Daily Use
```batch
# Just run this - it does everything!
start.bat
```

### Separate Services
```batch
# Start backend only
start_backend.bat

# Start frontend only (in another window)
start_frontend.bat
```

### Troubleshooting
```batch
# Reinstall backend
setup_backend.bat

# Reinstall frontend
setup_frontend.bat

# Re-download models
setup_hardware.bat

# Full reinstall
SETUP.bat
```

---

## 🌐 Browser Auto-Open

The following scripts automatically open your browser:
- ✅ `start.bat` - Opens to http://localhost:5173
- ✅ `start_frontend.bat` - Opens to http://localhost:5173

No need to manually type URLs!

---

## 💡 Tips

1. **Use `start.bat` for everything** - It's the easiest way to run FindMyPic
2. **Browser opens automatically** - No need to remember URLs
3. **Services run in background** - Minimized windows keep things clean
4. **Check the status** - Look at the launcher output for troubleshooting
5. **First run is slower** - AI models download once (5-10 minutes)
6. **After first run** - Starts in seconds, works offline

---

## 🆘 Common Issues

### "Python not found"
**Fix:** Install Python 3.10+ from https://python.org/downloads/
- Check "Add Python to PATH" during installation

### "Node.js not found"
**Fix:** Install Node.js 18+ from https://nodejs.org/

### "Backend won't start"
**Fix:**
1. Close any running Python processes
2. Run `setup_backend.bat` again

### "Frontend won't start"
**Fix:**
1. Delete `frontend\node_modules`
2. Run `setup_frontend.bat`

### "Models downloading slowly"
**Normal!** AI models are large (~750MB total). This happens once.

### "Browser doesn't open"
**Fix:** Manually open http://localhost:5173 in your browser
