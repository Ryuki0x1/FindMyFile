# 🔍 FindMyFile - Local AI File Search Engine

<div align="center">

<!-- Add a banner image here after creating one -->
# 🔍 FindMyFile

**100% Local | Private | Powerful**

Search your photos by what's in them, who's in them, or text in them.  
Everything runs on your computer. No cloud. Complete privacy.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)
[![Windows](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/yourusername/FindMyFile)

[Features](#-features) • [Quick Start](#-quick-start) • [How It Works](#-how-it-works) • [Privacy](#-privacy--security) • [Screenshots](#-screenshots--demo)

</div>

---

## 📸 What is FindMyFile?

FindMyFile is a **100% local** AI-powered file search engine that runs entirely on your computer. No internet required after setup!

### **Search your photos by:**
- 🖼️ **Visual Content** - "sunset beach", "red car", "white cat"
- 👤 **Faces** - Upload a face photo, find all photos of that person  
- 📝 **Text in Images** - Find receipts, bills, screenshots with specific text
- 📁 **Folder Filtering** - Search only in specific folders (10x faster!)
- 🎯 **Relevance Scoring** - Filter out low-quality matches

### **Why FindMyFile?**
✅ **100% Local** - Everything runs on your PC, no cloud  
✅ **Private** - Your photos never leave your computer  
✅ **Fast** - GPU-accelerated AI (CPU works too!)  
✅ **Free** - Open source, no subscriptions  
✅ **Smart** - Powered by CLIP, FaceNet, and EasyOCR  
✅ **Easy** - One-click setup with automatic GPU detection

---

## ✨ Features

### Core Features
- **🔍 Visual Search** - Search by describing what's in the image using natural language
- **👤 Face Recognition** - Upload a reference face and find all photos of that person
- **📝 OCR Text Search** - Find text inside images (receipts, screenshots, documents)
- **📁 Folder Filtering** - Search only specific folders for 10x faster results
- **🎯 Smart Scoring** - Filter by relevance score to get only high-quality matches
- **⚡ GPU Acceleration** - Automatic GPU detection for 10x faster indexing
- **💾 Local Storage** - ChromaDB vector database stores embeddings locally

### Advanced Features
- **🔄 Batch Processing** - Hardware-optimized batch sizes for efficient indexing
- **📊 Progress Tracking** - Real-time indexing progress with ETA
- **🖼️ Thumbnail Generation** - Automatic WebP thumbnail creation
- **📸 EXIF Metadata** - Extract camera info, date taken, location data
- **🎨 Modern UI** - Dark theme with glassmorphism design
- **🔒 Privacy First** - Zero telemetry, zero cloud, zero tracking

---

## 🚀 Quick Start

### Prerequisites
Before you begin, ensure you have:
- **Windows 10/11** (or macOS/Linux with minor script adjustments)
- **Python 3.10 or newer** - [Download here](https://www.python.org/downloads/)
- **Node.js 18 or newer** - [Download here](https://nodejs.org/)
- **8GB+ RAM** (16GB recommended for GPU version)
- **2GB free disk space** (10GB for GPU version + models)

### Installation

#### Option 1: Clone from GitHub (Recommended)
```bash
# Clone the repository
git clone https://github.com/[your-username]/FindMyFile.git
cd FindMyFile

# Run setup wizard (detects GPU, installs dependencies)
SETUP.bat
```

> **Note:** Replace `[your-username]` with your actual GitHub username after uploading.

#### Option 2: Download ZIP
1. Download the [latest release](https://github.com/yourusername/FindMyFile/releases)
2. Extract to a folder (e.g., `C:\FindMyFile`)
3. Run `SETUP.bat`

> **📦 AI Models:** FindMyPic does NOT ship with pre-downloaded AI models. All models (~540-850MB) are downloaded automatically on first use from official sources (HuggingFace, PyPI). This keeps the repository lightweight and ensures you get the latest models. See [MODEL_DOWNLOADS.md](MODEL_DOWNLOADS.md) for details.

### Setup Wizard

The `SETUP.bat` script will:
1. ✅ Check Python and Node.js installation
2. 🔍 Detect your GPU (NVIDIA/AMD/Intel/None)
3. 💡 Recommend CPU or GPU version based on hardware
4. 📦 Install Python dependencies (500MB CPU / 8.6GB GPU)
5. 🎨 Install frontend dependencies
6. 🧪 Test the installation
7. 🚀 Offer to launch immediately

**Estimated time:** 5-10 minutes (mostly downloading)

### Launch the Application

```batch
# Start both backend and frontend
start.bat
```

**First launch:**
- Detects your GPU and RAM
- **Automatically downloads and selects optimal AI models** based on your hardware:
  - **High-end GPU (8GB+ VRAM)**: Large CLIP model (~600MB) - Best accuracy
  - **Mid-range GPU (4-8GB VRAM)**: Base CLIP model (~350MB) - 40% smaller!
  - **Entry-level GPU (<4GB VRAM)**: Compact CLIP (~300MB) - 50% smaller!
  - **CPU only**: Optimized base model (~350MB) - Works anywhere
  - FaceNet (face recognition) - ~100MB (downloaded on first face search)
  - EasyOCR (text extraction) - ~50MB (downloaded on first OCR operation)
- Creates personalized config (batch sizes, model selection)
- Opens browser to http://localhost:5173

**Subsequent launches:**
- Models are cached locally, starts instantly
- No re-downloading needed
- Works 100% offline

**Your hardware, your models!** 🎯

> ℹ️ **Internet Required:** Only for initial model downloads (~540-850MB total). After that, FindMyPic works completely offline. Models are cached in `~/.cache/` and never included in the repository.

---

## 🔒 Privacy & Security

### 100% Local Operation

FindMyFile is designed with **privacy-first** principles:

#### ✅ **What Runs Locally:**
- **All AI Processing** - CLIP, FaceNet, and EasyOCR run on your PC
- **Vector Database** - ChromaDB stores embeddings in `data/chroma_db/`
- **Search Index** - All image metadata stored locally
- **Web Interface** - Frontend served from your computer
- **Thumbnails** - Generated and cached locally

#### ✅ **What Requires Internet (One-Time Only):**
- **Initial Setup** - Downloading Python/Node.js packages
- **AI Model Download** - First run downloads CLIP, FaceNet, EasyOCR models
- **That's it!** - After setup, works 100% offline

#### ❌ **What NEVER Happens:**
- ❌ Your photos are NEVER uploaded anywhere
- ❌ Search queries are NEVER sent to any server
- ❌ No telemetry, analytics, or tracking
- ❌ No cloud services required
- ❌ No accounts or login required
- ❌ No internet connection needed after setup

### Where Your Data Lives

```
FindMyFile/
├── data/                          # All your data is here
│   ├── chroma_db/                 # Vector embeddings (search index)
│   ├── thumbnails/                # Generated thumbnails
│   └── config.json                # Your settings
│
└── ~/.cache/huggingface/          # AI models (downloaded once)
    ├── clip-vit-large-patch14/
    ├── facenet-pytorch/
    └── easyocr/
```

**Your original photos are NEVER moved, copied, or modified.**  
FindMyFile only reads them to create searchable embeddings.

### Security Features

- 🔐 **No external connections** after initial setup
- 🔐 **No data collection** or telemetry
- 🔐 **Open source** - Audit the code yourself
- 🔐 **Local-only** - Backend only binds to `localhost:8000`
- 🔐 **Air-gapped operation** - Disconnect internet after setup, still works!

---

## 🛠️ How It Works

### Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                    Your Computer                     │
│                                                      │
│  ┌──────────────┐         ┌──────────────────────┐ │
│  │   Browser    │◄────────┤   React Frontend     │ │
│  │ (localhost:  │         │  (localhost:5173)    │ │
│  │   5173)      │         └──────────────────────┘ │
│  └──────────────┘                   │               │
│         │                           │               │
│         │ HTTP Requests             │               │
│         ▼                           ▼               │
│  ┌──────────────────────────────────────────────┐  │
│  │         FastAPI Backend (localhost:8000)     │  │
│  │                                               │  │
│  │  ┌─────────────┐  ┌─────────────┐           │  │
│  │  │ CLIP Model  │  │  FaceNet    │  ┌──────┐ │  │
│  │  │ (Images &   │  │  (Face      │  │ OCR  │ │  │
│  │  │  Text)      │  │Recognition) │  │Engine│ │  │
│  │  └─────────────┘  └─────────────┘  └──────┘ │  │
│  │                                               │  │
│  │  ┌──────────────────────────────────────┐   │  │
│  │  │       ChromaDB Vector Store          │   │  │
│  │  │  - Image embeddings (768-dim)        │   │  │
│  │  │  - Face embeddings (512-dim)         │   │  │
│  │  │  - OCR text & metadata               │   │  │
│  │  └──────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │        Your Photo Collection                 │  │
│  │   (Never moved or modified, only read)       │  │
│  │   D:\Photos\, C:\Users\...\Pictures\, etc.   │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
└─────────────────────────────────────────────────────┘

         ❌ NO INTERNET CONNECTION NEEDED ❌
```

### The Indexing Process

When you index a folder, FindMyFile:

1. **📁 Scans Files** - Finds all images in the selected folder(s)
2. **🖼️ Generates Thumbnails** - Creates WebP thumbnails for fast preview
3. **📸 Extracts Metadata** - Reads EXIF data (date, camera, location, etc.)
4. **🤖 AI Processing** (the magic happens here):
   - **CLIP** creates a 768-dimensional vector representation of the image
   - **FaceNet** detects faces and creates 512-dim embeddings for each
   - **EasyOCR** extracts any text found in the image
5. **💾 Stores Embeddings** - Saves vectors to ChromaDB for fast searching
6. **✅ Ready to Search** - Your photos are now searchable!

**Example:** A photo of "sunset on beach" gets converted to a vector that's mathematically similar to the text "sunset on beach". When you search for that phrase, the vectors are compared using cosine similarity.

### The Search Process

When you search:

1. **📝 Your Query** - You type "sunset beach" or upload a face photo
2. **🔄 Embedding** - Query is converted to a vector using the same AI models
3. **🔍 Vector Search** - ChromaDB finds images with similar vectors (cosine similarity)
4. **📊 Scoring** - Results ranked by relevance (0-100%)
5. **🎯 Filtering** - Applied filters (folder, file type, min score)
6. **📤 Results** - Top matches returned to your browser

**All of this happens on your PC in milliseconds!**

---

## 💻 System Requirements

### Minimum (CPU Version)
- **OS:** Windows 10/11, macOS, or Linux
- **RAM:** 8 GB
- **Storage:** 2 GB free space
- **Python:** 3.10 or newer
- **Node.js:** 18 or newer (for web UI)

### Recommended (GPU Version)
- **GPU:** NVIDIA with 4GB+ VRAM
- **RAM:** 16 GB
- **Storage:** 10 GB free space (includes CUDA PyTorch)

**Good for:** Up to 50,000 photos  
**Fast for:** Up to 10,000 photos (on CPU)

---

## 📖 How to Use

### First Time: Index Your Photos

1. **Launch FindMyFile** (run `START.bat`)
2. **Click "Index Folder"** in the web UI
3. **Select your photo folder** (e.g., `D:\Photos`)
4. **Wait for indexing** (progress bar shows ETA)

**Indexing time:**
- CPU: ~1,000 photos/hour
- GPU: ~10,000 photos/hour

### Search Your Photos

#### Text Search
```
Search: "sunset beach"
→ Finds images with sunsets and beaches
```

#### Face Search
1. Click "Face Search" tab
2. Upload a clear face photo
3. Click "Find Matches"
→ Finds all photos with that person

#### Text-in-Image Search
```
Search: "GYM BILL"
→ Finds receipts, bills, documents with that text
```

### Advanced Filters

**Filter by score:**
```
Search: "cat"
Min Score: 70
→ Only shows results >70% confident
```

**Filter by folder:**
```
Search: "vacation photo"
Folder: D:\Photos\2024\Summer
→ Only searches that folder (10x faster!)
```

**Combine filters:**
```
Search: "family photo"
Folder: D:\Photos\2024
Min Score: 75
File Type: Image
→ Ultra-precise results!
```

---

## 🛠️ Folder Structure

```
FindMyFile/
├── SETUP.bat           ← Run this first (one time)
├── START.bat           ← Run this to launch
├── backend/            ← Python AI server
│   ├── .venv/          ← Python packages (created by setup)
│   └── app/            ← Backend code
├── frontend/           ← Web UI (React)
│   └── dist/           ← Built UI files
├── data/               ← Your data (created on first run)
│   ├── chroma_db/      ← Vector database (image embeddings)
│   ├── thumbnails/     ← Image thumbnails
│   └── config.json     ← Your personalized settings
└── README.md           ← This file
```

---

## 🎯 Usage Guide

### First Time: Index Your Photos

1. **Launch FindMyFile** - Run `start.bat`
2. **Open the web UI** - Browser opens automatically to `http://localhost:5173`
3. **Click "Index Folder"** or the settings icon
4. **Select your photo folder** - Browse to `D:\Photos` or wherever your images are
5. **Wait for indexing** - Progress bar shows:
   - Files processed
   - Faces detected
   - OCR text extracted
   - Estimated time remaining

**Indexing Performance:**
- **CPU:** ~1,000 photos/hour
- **GPU:** ~10,000 photos/hour

### Search Your Photos

#### **Visual Search (CLIP)**
Just describe what you're looking for:
```
Search: "sunset on the beach"
Search: "red car in parking lot"
Search: "white cat sitting on couch"
Search: "group of people at restaurant"
```

#### **Face Search**
1. Click the **"Face Search"** tab
2. Upload a clear face photo (frontal works best)
3. Click **"Find Matches"**
4. See all photos with that person

#### **Text Search (OCR)**
Find text inside images:
```
Search: "GYM BILL"
Search: "invoice"
Search: "receipt 2024"
```

### Using Search Filters

Click the **"Filters"** button to access advanced options:

#### **Folder Filter** (10x Faster!)
```
Folder Path: D:\Photos\2024\Summer
→ Only searches that specific folder
```

#### **Minimum Score Filter**
```
Min Score: 70%
→ Only shows results with 70%+ relevance
```

**Recommended thresholds:**
- `0%` - Show all results
- `60%` - Balanced (recommended)
- `70%` - Stricter quality
- `80%` - Very high quality only

#### **File Type Filter**
```
File Type: Images
→ Only image files (.jpg, .png, etc.)

File Type: Documents
→ Only documents (.pdf, .docx, etc.)
```

#### **Extension Filter**
```
Extension: .jpg
→ Only JPG files
```

### Combine Multiple Filters

Get ultra-precise results:
```
Query: "family photo"
Folder: D:\Photos\2024\Birthday
Min Score: 75%
File Type: Images
Extension: .jpg

→ High-quality family photos from birthday folder, JPGs only
```

---

## 🐛 Troubleshooting

### Setup Issues

#### "Python not found"
**Solution:**
1. Download Python from https://python.org/downloads/
2. **Important:** Check "Add Python to PATH" during installation
3. Restart your terminal/command prompt
4. Run `SETUP.bat` again

#### "Node.js not found"
**Solution:**
1. Download Node.js LTS from https://nodejs.org/
2. Install with default options
3. Restart terminal
4. Run `SETUP.bat` again

#### "Setup failed - pip install errors"
**Solution:**
```batch
# Delete virtual environment and try again
cd backend
rmdir /s /q .venv
cd ..
SETUP.bat
```

### Runtime Issues

#### "Backend won't start"
**Solution:**
```batch
# Close all Python processes
taskkill /f /im python.exe

# Restart
start.bat
```

#### "Frontend won't start / Port already in use"
**Solution:**
```batch
# Close processes on port 5173
netstat -ano | findstr :5173
taskkill /f /pid <PID_FROM_ABOVE>

# Restart
start.bat
```

#### "Models downloading slowly"
**This is normal!** AI models are large (~750MB total). This only happens once on first run. Future launches are instant.

#### "Search returns weird results"
**Solution:** Use the minimum score filter:
```
Click Filters → Set Min Score to 70%
```

Lower scores often include unrelated images. Start with 60-70% for best results.

#### "Out of memory during indexing"
**Solution:**
1. Close other applications
2. Index smaller folders at a time (split large collections)
3. Use CPU version instead of GPU (uses less RAM)

#### "Face search not finding anyone"
**Check:**
- Is the reference face photo clear and frontal?
- Are faces visible in the photos being searched?
- Try re-indexing - faces are detected during indexing

### Performance Issues

#### "Indexing is slow"
**CPU Version:**
- Expected: ~1,000 photos/hour
- Normal for computers without NVIDIA GPU

**GPU Version:**
- Expected: ~10,000 photos/hour
- Check GPU is detected: Look for "GPU: NVIDIA..." in backend startup

**Speed it up:**
- Close other programs
- Use GPU version if you have NVIDIA graphics card
- Index during off-hours (can run overnight)

#### "Search is slow"
**Solution:** Use folder filtering
```
Folder Path: D:\Photos\2024
→ Searches only that folder (10x faster!)
```

### Common Questions

#### "Can I index external drives?"
Yes! Just select the folder from your external drive during indexing. Keep the drive connected for searching.

#### "Can I index multiple folders?"
Yes! Index each folder separately. They all get added to the same searchable database.

#### "What if I move photos after indexing?"
You'll need to re-index. The paths are stored in the database.

#### "Can I delete the index and start over?"
Yes:
```batch
# Delete database
rmdir /s /q data\chroma_db

# Re-index your folders
```

#### "Does this work on Mac/Linux?"
Yes! The Python/Node.js code is cross-platform. You'll need to:
1. Convert `.bat` scripts to `.sh` (bash scripts)
2. Adjust paths (`\` → `/`)

---

## ❓ FAQ

### Q: Does this require internet?
**A:** Only for initial setup (downloading AI models). After that, works 100% offline.

### Q: Where are my photos stored?
**A:** They stay where they are! FindMyFile only reads them and creates a search index. Your originals are never moved or modified.

### Q: What is "indexing"?
**A:** Creating a searchable database of your photos. FindMyFile reads each photo once, creates an AI "fingerprint" (embedding), and stores it for fast searching later.

### Q: How much storage does it use?
**A:** About 1KB per photo for the search index. 10,000 photos ≈ 10MB of database.

### Q: Can I index multiple folders?
**A:** Yes! Index as many folders as you want. They all get added to the same searchable database.

### Q: CPU or GPU version?
**A:** 
- **CPU:** Works on any computer, good for <10,000 photos
- **GPU:** Requires NVIDIA GPU, 10x faster, great for 50,000+ photos

The setup wizard auto-detects and recommends the best version for you.

### Q: Is my data private?
**A:** 100% YES. Everything runs locally. No cloud. No internet (after setup). No tracking. Your photos never leave your computer.

### Q: Can I use this on Mac or Linux?
**A:** Yes! The Python code works on all platforms. You'll need to adapt the `.bat` scripts to `.sh` for Mac/Linux.

---

## 🔧 Troubleshooting

### "Python not found"
**Fix:** Install Python from https://python.org/downloads/  
Make sure to check "Add Python to PATH" during installation.

### "Node.js not found"
**Fix:** Install Node.js from https://nodejs.org/  
Choose the LTS (Long Term Support) version.

### "Backend won't start"
**Fix:** 
1. Close any running Python processes
2. Run `SETUP.bat` again
3. Check the backend window for error messages

### "Models downloading slowly"
**Normal!** AI models are large (~750MB total). This happens once. Future launches are instant.

### "Search returns weird results"
**Fix:** Use the minimum score filter:
```
Search: "cat"
Min Score: 70  ← Add this
```

### "Out of memory during indexing"
**Fix:** The setup wizard automatically configures batch sizes for your RAM. If you still get errors:
1. Close other programs
2. Index smaller folders at a time
3. Use the CPU version (smaller memory footprint)

---

## 📸 Screenshots & Demo

<!-- 
Add screenshots here after capturing them:

### Main Search Interface
![Search Interface](docs/screenshots/search-interface.png)
*Beautiful dark theme with glassmorphism design*

### Search Filters
![Search Filters](docs/screenshots/search-filters.png)
*Folder filtering, min score slider, file type dropdown*

### Search Results
![Search Results](docs/screenshots/search-results.png)
*Grid view with relevance scores and metadata*

### Face Search
![Face Search](docs/screenshots/face-search.png)
*Upload a face and find all matching photos*

### Indexing Progress
![Indexing Progress](docs/screenshots/indexing-progress.png)
*Real-time progress with ETA and stats*

**Note:** Screenshots will be added in a future update.
-->

---

## 🗂️ Project Structure

```
FindMyFile/
│
├── 📄 README.md                    # This file
├── 📄 PROJECT_STRUCTURE.md         # Detailed structure guide
├── 🚀 SETUP.bat                    # One-click setup wizard
├── 🚀 start.bat                    # Application launcher
│
├── 📂 backend/                     # Python FastAPI backend
│   ├── requirements.txt            # GPU version dependencies
│   ├── requirements-runtime.txt    # CPU version dependencies
│   ├── requirements-dev.txt        # Development dependencies
│   │
│   └── app/
│       ├── main.py                 # FastAPI entry point
│       │
│       ├── api/                    # API endpoints
│       │   ├── search.py           # Search endpoints
│       │   ├── index.py            # Indexing endpoints
│       │   └── settings.py         # Settings endpoints
│       │
│       ├── ai/                     # AI models
│       │   ├── clip_embed.py       # CLIP image/text embeddings
│       │   ├── face_embed.py       # FaceNet face recognition
│       │   └── ocr_engine.py       # EasyOCR text extraction
│       │
│       ├── core/                   # Core business logic
│       │   ├── indexer.py          # Folder scanning & indexing
│       │   ├── searcher.py         # Search engine
│       │   ├── metadata.py         # EXIF & metadata extraction
│       │   ├── first_run.py        # Hardware detection wizard
│       │   └── config.py           # Configuration management
│       │
│       ├── db/                     # Database layer
│       │   └── vector_store.py     # ChromaDB wrapper
│       │
│       └── models/                 # Data schemas
│           └── schemas.py          # Pydantic models
│
├── 📂 frontend/                    # React + TypeScript frontend
│   ├── package.json                # Node.js dependencies
│   ├── vite.config.ts              # Vite configuration
│   │
│   └── src/
│       ├── App.tsx                 # Main app component
│       │
│       ├── components/             # React components
│       │   ├── SearchBar.tsx       # Search input & history
│       │   ├── SearchFilters.tsx   # Advanced filters UI
│       │   ├── ResultsGrid.tsx     # Search results display
│       │   ├── FilePreview.tsx     # Image preview modal
│       │   ├── FaceSearch.tsx      # Face search interface
│       │   └── OnboardingFlow.tsx  # First-run setup wizard
│       │
│       └── services/
│           └── api.ts              # API client (typed)
│
├── 📂 data/                        # User data (created at runtime)
│   ├── chroma_db/                  # Vector database
│   ├── thumbnails/                 # Generated thumbnails
│   └── config.json                 # User settings
│
└── 📂 docs/                        # Developer documentation
    ├── PROGRESS.md                 # Development progress
    ├── PRD.md                      # Product requirements
    ├── DEPLOYMENT.md               # Deployment guide
    └── IMPROVEMENTS_SUMMARY.md     # Technical improvements
```

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Reporting Bugs
1. Check if the issue already exists in [Issues](https://github.com/yourusername/FindMyFile/issues)
2. Create a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Your system info (OS, Python version, GPU)
   - Error messages or logs

### Suggesting Features
1. Open an issue with the "enhancement" label
2. Describe the feature and why it's useful
3. Include examples or mockups if possible

### Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages (`git commit -m 'Add amazing feature'`)
6. Push to your fork (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/FindMyFile.git
cd FindMyFile

# Install dependencies
SETUP.bat

# Run in development mode
start.bat
```

### Code Style
- **Python:** Follow PEP 8, use type hints
- **TypeScript:** Use ESLint configuration
- **Commits:** Clear, descriptive messages

---

## 🛣️ Roadmap

### ✅ Phase 1 - MVP (Completed)
- [x] Visual search (CLIP)
- [x] Backend (FastAPI)
- [x] Frontend (React + TypeScript)
- [x] Vector database (ChromaDB)
- [x] End-to-end integration

### ✅ Phase 2 - Document Support (Completed)
- [x] OCR integration (EasyOCR)
- [x] Face recognition (FaceNet)
- [x] Face search UI
- [x] Search filters UI
- [x] Folder-specific search
- [x] Minimum score filtering

### 🔜 Phase 3 - Polish & Power Features (In Progress)
- [ ] Document text extraction (DOCX, XLSX, TXT)
- [ ] Incremental indexing (only re-index changed files)
- [ ] File system watcher (auto-index new files)
- [ ] Dark/Light theme toggle
- [ ] Search history & saved searches
- [ ] Export search results

### 🔮 Phase 4 - Advanced (Future)
- [ ] LLaVA/Moondream image captioning
- [ ] Multi-language OCR support
- [ ] Video frame search
- [ ] Duplicate detection
- [ ] Smart albums / auto-categorization
- [ ] Desktop app (Electron packaging)

See [PROGRESS.md](docs/PROGRESS.md) for detailed status.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 FindMyFile Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 🙏 Acknowledgments

### AI Models
- **CLIP** - OpenAI's Contrastive Language-Image Pre-training
- **FaceNet** - Google's face recognition model
- **EasyOCR** - Jaided AI's OCR engine

### Technologies
- **FastAPI** - Modern Python web framework
- **React** - UI library
- **ChromaDB** - Vector database
- **PyTorch** - Deep learning framework
- **Vite** - Frontend build tool

### Inspiration
Built for privacy-conscious users who want powerful AI File Search without sacrificing their data to cloud services.

---

## 📞 Support & Community

- 📖 **Documentation:** [docs/](docs/)
- 🐛 **Bug Reports:** [GitHub Issues](../../issues)
- 💬 **Discussions:** [GitHub Discussions](../../discussions)
- ⭐ **Star this repo** if you find it useful!

---

## 🌟 Star History

If FindMyFile helps you, please consider giving it a star! ⭐

---

<div align="center">

**Made with ❤️ for privacy-focused photo enthusiasts**

[Report Bug](../../issues) • [Request Feature](../../issues) • [Documentation](docs/)

</div>

---

## 📚 More Information

- **Technical Details:** See `IMPROVEMENTS_SUMMARY.md`
- **Deployment Guide:** See `DEPLOYMENT.md`
- **Project Roadmap:** See `PRD.md`
- **Build Progress:** See `PROGRESS.md`

---

## 🆘 Getting Help

1. Check the FAQ above
2. Look at error messages in the backend/frontend windows
3. Review `PROGRESS.md` for known issues

---

## 🎯 Tips for Best Results

### Organize Your Photos
```
D:\Photos\
  ├── 2024\
  │   ├── Summer_Vacation\
  │   ├── Work_Events\
  │   └── Family\
  └── 2023\
      └── ...
```
Then use folder filters for faster, more accurate searches!

### Use Specific Search Terms
```
❌ Vague: "photo"
✅ Better: "beach sunset with palm trees"

❌ Vague: "person"
✅ Better: "group photo at restaurant"
```

### Leverage Face Search
Upload a clear, frontal face photo for best results. Profile shots work but are less accurate.

### Combine Multiple Filters
```
Search: "birthday"
Folder: D:\Photos\2024\March
Min Score: 75
File Type: Image
```

### Re-index After Major Changes
If you add/remove many photos, re-index that folder to update the database.

---

## 🎉 You're Ready!

1. ✅ Read this guide
2. 🚀 Run `SETUP.bat`
3. 🎬 Run `START.bat`
4. 🔍 Start searching!

**Enjoy your AI-powered file search!** 📸✨

---

**Made with ❤️ for privacy-focused photo enthusiasts**
