# FindMyPic - Complete User Guide

Welcome to FindMyPic! This guide will help you get started with your AI-powered local photo search engine.

## 📚 Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [First Launch](#first-launch)
- [Using FindMyPic](#using-findmypic)
- [Features](#features)
- [Troubleshooting](#troubleshooting)
- [Advanced Usage](#advanced-usage)
- [FAQ](#faq)

---

## 🚀 Quick Start

**3 Simple Steps:**

```batch
# 1. Clone the repository
git clone https://github.com/Ryuki0x1/FindMyFile.git
cd FindMyFile

# 2. Run setup (detects hardware, downloads AI models)
SETUP.bat

# 3. Start FindMyPic (browser opens automatically!)
start.bat
```

That's it! The browser will open automatically to http://localhost:5173

---

## 💾 Installation

### Prerequisites

Before installing FindMyPic, make sure you have:

1. **Python 3.10 or newer**
   - Download from: https://www.python.org/downloads/
   - ⚠️ **IMPORTANT:** Check "Add Python to PATH" during installation!

2. **Node.js 18 or newer**
   - Download from: https://nodejs.org/
   - Get the LTS (Long Term Support) version

3. **At least 2GB free disk space**
   - For AI models (~540-850MB)
   - For dependencies (~500MB-8.6GB depending on GPU/CPU version)

4. **Internet connection**
   - Required for initial setup and model downloads
   - After setup, FindMyPic works 100% offline!

### Installation Steps

#### Option 1: Clone from GitHub (Recommended)

```batch
# Clone the repository
git clone https://github.com/Ryuki0x1/FindMyFile.git
cd FindMyFile

# Run the setup wizard
SETUP.bat
```

The setup wizard will:
1. Detect your hardware (GPU, RAM, CPU)
2. Install Python dependencies
3. Download optimal AI models for your hardware
4. Install frontend dependencies
5. Create personalized configuration

**Time required:** 10-15 minutes (depending on internet speed)

#### Option 2: Download ZIP

1. Download from: https://github.com/Ryuki0x1/FindMyFile
2. Click "Code" → "Download ZIP"
3. Extract to a folder (e.g., `C:\FindMyPic`)
4. Open the folder and run `SETUP.bat`

---

## 🎬 First Launch

### What Happens on First Launch?

When you run `SETUP.bat` for the first time:

**1. Hardware Detection (30 seconds)**
   - Detects your NVIDIA GPU (if available)
   - Measures available RAM
   - Determines optimal model tier

**2. Backend Setup (3-5 minutes)**
   - Creates Python virtual environment
   - Installs dependencies
   - Detects if you have GPU or CPU only

**3. Model Download (5-10 minutes)**
   - **CLIP Model** (300-600MB) - Image understanding
   - **FaceNet Model** (~100MB) - Face recognition
   - **Text Embedder** (~90MB) - Document search
   - Models are cached locally for offline use

**4. Frontend Setup (2-3 minutes)**
   - Installs npm packages
   - Sets up React development server

**5. Configuration**
   - Creates `data/config.json` with optimal settings
   - Saves your hardware profile

### Model Selection Based on Hardware

FindMyPic automatically selects the best models for your system:

| Hardware | Model Size | CLIP Model | Performance |
|----------|-----------|------------|-------------|
| **High-end GPU** (8GB+ VRAM) | ~850MB | Large (patch14) | Best accuracy |
| **Mid-range GPU** (4-8GB VRAM) | ~540MB | Base (patch32) | Balanced |
| **Entry GPU** (<4GB VRAM) | ~540MB | Base (patch32) | Good |
| **CPU Only** | ~540MB | Base (patch32) | Good |

---

## 🎯 Using FindMyPic

### Starting the Application

```batch
# Start everything (recommended)
start.bat
```

The browser will automatically open to http://localhost:5173 when ready!

**Alternative start methods:**

```batch
# Start backend only (API server)
start_backend.bat

# Start frontend only (in another window)
start_frontend.bat
```

### Stopping the Application

**Easy way:**
- Close the minimized windows titled "FindMyPic Backend" and "FindMyPic Frontend"

**Alternative:**
- Press `Ctrl+C` in each window
- Or simply close the command prompt windows

---

## ✨ Features

### 1. Natural Language Search

Search your photos using everyday language:

**Examples:**
- "sunset at the beach"
- "red car parked outside"
- "my dog playing in the park"
- "birthday party with cake"
- "mountains covered in snow"

No need for tags or keywords - the AI understands what you're looking for!

### 2. Face Search

Find photos of specific people:

1. Click **"Face Search"** tab
2. Upload a reference photo of the person
3. FindMyPic finds all photos containing that person

**Use cases:**
- Find all photos of a family member
- Locate photos from a specific event
- Organize photos by people

### 3. Text Search (OCR)

Find photos containing specific text:

**Examples:**
- "street signs"
- "restaurant menu"
- "birthday card"
- "business card"
- "whiteboard notes"

FindMyPic extracts and searches text within images!

### 4. Advanced Filters

Refine your search with filters:

- **File Type:** JPG, PNG, GIF, BMP, etc.
- **Date Range:** Find photos from specific periods
- **File Size:** Filter by image size
- **Dimensions:** Search by resolution

### 5. Batch Operations

Work with multiple photos:

- **Select Multiple:** Click checkboxes on search results
- **Export Selected:** Save selected photos to a folder
- **Tag Selected:** Add tags for organization
- **Delete Selected:** Remove unwanted photos

---

## 📁 Indexing Your Photos

Before searching, you need to index your photos:

### How to Index

1. **Open Settings** (gear icon in top-right)
2. **Add Folders** to index
   - Click "Add Folder"
   - Browse to your photo directory
   - Examples: `C:\Users\YourName\Pictures`, `D:\Photos`
3. **Click "Start Indexing"**

### Indexing Process

**What happens:**
1. FindMyPic scans all images in selected folders
2. AI analyzes each image (CLIP embeddings)
3. Faces are detected and embedded (if face search enabled)
4. Text is extracted (if OCR enabled)
5. Metadata is stored in local database

**Time required:**
- ~1-2 seconds per image (CPU)
- ~0.3-0.5 seconds per image (GPU)

**For 1,000 photos:**
- CPU: ~15-30 minutes
- GPU: ~5-8 minutes

### Incremental Indexing

FindMyPic only indexes new or changed photos:
- Add new photos to indexed folders
- Click "Reindex" in Settings
- Only new photos are processed

---

## 🎛️ Settings & Configuration

### Optimizations Tab

**Batch Size:** Number of images processed at once
- Higher = Faster (requires more RAM/VRAM)
- Lower = Slower (uses less memory)
- Auto-detected based on your hardware

**Model Selection:**
- View your current AI models
- See hardware-optimized settings

### Indexed Folders

**Add/Remove Folders:**
- Manage which folders are indexed
- Remove folders to free up database space

**Reindex:**
- Update index after adding new photos
- Refresh embeddings with newer models

### Advanced Settings

**CLIP Model Override:**
```json
{
  "optimizations": {
    "clip_model": "openai/clip-vit-large-patch14"
  }
}
```

Edit `data/config.json` to customize.

---

## 🔧 Troubleshooting

### Common Issues

#### "Python not found"

**Problem:** Python is not installed or not in PATH

**Fix:**
1. Install Python from https://python.org/downloads/
2. During installation, **check** "Add Python to PATH"
3. Restart your computer
4. Run `SETUP.bat` again

---

#### "Node.js not found"

**Problem:** Node.js is not installed

**Fix:**
1. Install Node.js from https://nodejs.org/
2. Download the LTS version
3. Restart your computer
4. Run `SETUP.bat` again

---

#### "Backend won't start"

**Problem:** Port 8000 is already in use or Python error

**Fix:**
1. Close any running Python processes
2. Check if another app is using port 8000
3. Run `setup_backend.bat` to reinstall
4. Check `backend/.venv/` exists

---

#### "Frontend won't start"

**Problem:** Port 5173 is already in use or npm error

**Fix:**
1. Close any running Vite/Node processes
2. Delete `frontend/node_modules`
3. Run `setup_frontend.bat`
4. Try `npm cache clean --force`

---

#### "Models downloading very slowly"

**Problem:** Large AI models can take time to download

**This is normal!**
- Models are 540-850MB total
- HuggingFace servers can be slow
- Download happens only once
- After first download, models are cached

**Fix:**
- Be patient (5-10 minutes)
- Check internet connection
- Some corporate networks block HuggingFace - try VPN

---

#### "Search returns no results"

**Problem:** Photos not indexed or wrong query

**Fix:**
1. Make sure you've indexed your photo folders (Settings → Indexing)
2. Wait for indexing to complete
3. Try different search terms
4. Check that photos are in indexed folders

---

#### "Out of memory error"

**Problem:** Batch size too large for your RAM/VRAM

**Fix:**
1. Open `data/config.json`
2. Reduce `batch_size` value (try 8, then 4, then 2)
3. Restart the application
4. Example:
```json
{
  "optimizations": {
    "batch_size": 4
  }
}
```

---

#### "GPU not detected"

**Problem:** NVIDIA GPU not recognized

**Fix:**
1. Install latest NVIDIA drivers
2. Verify `nvidia-smi` works in command prompt
3. CPU version works fine too! (just slower)

---

### Getting Help

**Still having issues?**

1. **Check the logs:**
   - Backend: Look in the "FindMyPic Backend" window
   - Frontend: Look in the "FindMyPic Frontend" window

2. **Restart everything:**
   ```batch
   # Close all windows, then:
   start.bat
   ```

3. **Full reinstall:**
   ```batch
   # Delete these folders:
   # - backend\.venv
   # - frontend\node_modules
   
   # Then run:
   SETUP.bat
   ```

4. **Report an issue:**
   - GitHub: https://github.com/Ryuki0x1/FindMyFile/issues
   - Include error messages and system info

---

## 🚀 Advanced Usage

### Custom Model Configuration

Edit `data/config.json` to customize:

```json
{
  "optimizations": {
    "clip_model": "openai/clip-vit-large-patch14",
    "batch_size": 16,
    "use_gpu": true,
    "model_tier": "high"
  }
}
```

### Command Line Usage

**Start backend only:**
```batch
cd backend
.venv\Scripts\activate
python -m app.main
```

**Start frontend only:**
```batch
cd frontend
npm run dev
```

### API Access

Access the FastAPI backend directly:

- **API Base:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **OpenAPI Schema:** http://localhost:8000/openapi.json

**Example API calls:**
```python
import requests

# Search for images
response = requests.post('http://localhost:8000/api/search', json={
    'query': 'sunset at the beach',
    'limit': 10
})
results = response.json()

# Get image by ID
response = requests.get('http://localhost:8000/api/image/123')
```

### Database Location

FindMyPic stores data in:
- **Windows:** `data/` folder in project root
- **Database:** `data/findmypic.db` (SQLite)
- **Embeddings:** `data/embeddings/` (NumPy arrays)

**Backup your data:**
```batch
# Copy the entire data folder
xcopy /E /I data data_backup
```

---

## ❓ FAQ

### General Questions

**Q: Does FindMyPic work offline?**  
A: Yes! After the initial setup and model download, FindMyPic works 100% offline. No internet required.

**Q: Is my data private?**  
A: Absolutely! Everything runs locally on your computer. No data is sent to any server. Your photos never leave your machine.

**Q: How accurate is the AI search?**  
A: Very accurate! FindMyPic uses OpenAI's CLIP model, which understands both images and text remarkably well.

**Q: Can I search multiple folders?**  
A: Yes! Add as many folders as you want in Settings → Indexed Folders.

**Q: Does it modify my original photos?**  
A: No! FindMyPic only reads your photos. It never modifies, moves, or deletes original files (unless you explicitly delete via the UI).

### Technical Questions

**Q: What file formats are supported?**  
A: JPG, JPEG, PNG, GIF, BMP, TIFF, WEBP

**Q: How much disk space does it need?**  
A: 
- AI models: 540-850MB (cached in `~/.cache/`)
- Database: ~1MB per 1,000 photos
- Dependencies: 500MB-8.6GB (backend `.venv` folder)

**Q: Can I use it on multiple computers?**  
A: Yes! Clone the repo on each computer and run `SETUP.bat`. The `data/` folder can be synced (e.g., via cloud storage) to share your indexed database.

**Q: Does it support video search?**  
A: Not yet, but it's planned for future releases!

**Q: Can I run it on Linux/Mac?**  
A: The Python backend works on Linux/Mac, but the batch files are Windows-only. You'll need to run setup/start commands manually. Linux/Mac support coming soon!

### Performance Questions

**Q: How many photos can it handle?**  
A: 
- **CPU:** Up to 10,000 photos (smooth performance)
- **GPU:** 50,000+ photos (very fast)
- Database scales well to hundreds of thousands

**Q: Why is the first search slow?**  
A: The first search loads AI models into memory. Subsequent searches are much faster!

**Q: Can I speed up indexing?**  
A: 
- Use a GPU (3-5x faster than CPU)
- Increase batch size (if you have enough RAM)
- Close other applications during indexing

---

## 📖 Additional Resources

- **GitHub Repository:** https://github.com/Ryuki0x1/FindMyFile
- **Model Downloads Guide:** [MODEL_DOWNLOADS.md](MODEL_DOWNLOADS.md)
- **Batch Files Reference:** [BATCH_FILES_GUIDE.md](BATCH_FILES_GUIDE.md)
- **Project Structure:** [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- **Contributing:** [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🎉 Enjoy FindMyPic!

Thank you for using FindMyPic! We hope it makes managing your photo collection effortless and enjoyable.

**Happy searching! 📸🔍**

---

*Last updated: February 26, 2026*  
*Version: 1.0.0*
