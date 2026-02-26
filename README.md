# 🔍 FindMyPic - AI-Powered Photo Search

**100% Local | Private | Powerful**

Search your photos using AI - by visual content, faces, or text. Everything runs on your computer. No cloud, complete privacy.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)

---

## ✨ Features

- 🔍 **Visual Search** - "sunset beach", "red car", "white cat"
- 👤 **Face Recognition** - Upload a face, find all photos of that person
- 📝 **OCR Text Search** - Find text inside images (receipts, screenshots)
- ⚡ **GPU Accelerated** - Automatic GPU detection, 10x faster indexing
- 🔒 **100% Private** - Everything runs locally, no cloud, no tracking
- 💾 **Offline** - Works completely offline after initial setup

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+** - [Download](https://python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **8GB+ RAM** (16GB recommended for GPU)

### Installation

```bash
# Clone the repository
git clone https://github.com/Ryuki0x1/FindMyFile.git
cd FindMyFile

# Run setup (10-15 minutes)
SETUP.bat
```

The setup wizard will:
1. ✅ Check Python & Node.js
2. ✅ Detect GPU and install dependencies
3. ✅ Download AI models (~540-850MB, happens once)
4. ✅ Offer to launch the app

### Launch

```bash
start.bat
```

Browser opens automatically to http://localhost:5173

---

## 📖 How to Use

1. **Index Your Photos**
   - Settings → Add folders to index
   - Click "Start Indexing"
   - Wait for AI to analyze your photos

2. **Search**
   - **Visual**: Type "sunset at beach"
   - **Face**: Upload a reference photo
   - **Text**: Search for text in images

3. **Filter Results**
   - By folder, file type, date, score

---

## 🔒 Privacy & Security

- ✅ 100% local - Everything runs on your PC
- ✅ No cloud - Your photos never leave your computer
- ✅ No tracking - Zero telemetry or analytics
- ✅ Offline - Works without internet after setup
- ✅ Open source - Audit the code yourself

**Your photos stay where they are. FindMyPic only reads them to create a searchable index.**

---

## 💻 System Requirements

### Minimum (CPU)
- 8GB RAM
- 2GB free disk space
- Good for up to 10,000 photos

### Recommended (GPU)
- NVIDIA GPU with 4GB+ VRAM
- 16GB RAM
- 10GB free disk space
- Great for 50,000+ photos

---

## 🛠️ How It Works

1. **Indexing**: AI models analyze each photo and create "embeddings" (mathematical representations)
2. **Storage**: Embeddings stored in local vector database (ChromaDB)
3. **Search**: Your query is converted to an embedding and matched against stored photos
4. **Results**: Most similar photos ranked by relevance

**AI Models Used:**
- **CLIP** (OpenAI) - Understands images and text
- **FaceNet** (Google) - Face recognition
- **EasyOCR** - Text extraction from images

---

## 📁 Project Structure

```
FindMyPic/
├── SETUP.bat              # One-click setup
├── start.bat              # Launch app (auto-opens browser)
│
├── backend/               # Python FastAPI backend
│   ├── app/
│   │   ├── ai/           # AI models (CLIP, FaceNet, OCR)
│   │   ├── api/          # REST API endpoints
│   │   ├── core/         # Business logic
│   │   └── db/           # ChromaDB vector store
│   └── requirements.txt
│
├── frontend/              # React + Vite frontend
│   ├── src/
│   │   ├── components/   # UI components
│   │   ├── pages/        # Main pages
│   │   └── services/     # API client
│   └── package.json
│
└── data/                  # Your data (gitignored)
    ├── chroma_db/        # Vector embeddings
    ├── thumbnails/       # Generated thumbnails
    └── config.json       # Your settings
```

---

## 🔧 Troubleshooting

### "Python not found"
Install Python 3.10+ from https://python.org/downloads/  
**Check "Add Python to PATH" during installation**

### "Node.js not found"
Install Node.js 18+ from https://nodejs.org/

### "Models downloading slowly"
This is normal! AI models are ~750MB total. Happens once, then cached.

### "Backend won't start"
```bash
# Close Python processes and restart
taskkill /f /im python.exe
start.bat
```

### "Search returns no results"
- Make sure you've indexed your photos (Settings → Indexing)
- Try different search terms
- Adjust minimum score filter

---

## 📚 Documentation

- **[Complete User Guide](USER_GUIDE.md)** - Detailed usage instructions
- **[Model Downloads](MODEL_DOWNLOADS.md)** - AI model information
- **[Contributing](CONTRIBUTING.md)** - How to contribute
- **[Project Structure](PROJECT_STRUCTURE.md)** - Codebase details
- **[Changelog](CHANGELOG.md)** - Version history

---

## ❓ FAQ

**Q: Does it work offline?**  
A: Yes! After initial setup, 100% offline.

**Q: Where are my photos stored?**  
A: They stay where they are. FindMyPic only reads them.

**Q: How much storage does it use?**  
A: ~1KB per photo for the index. 10,000 photos ≈ 10MB.

**Q: CPU or GPU version?**  
A: Setup wizard auto-detects and recommends the best for your hardware.

**Q: Is my data private?**  
A: 100% YES. Everything runs locally. No cloud, no internet (after setup), no tracking.

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

## 🙏 Acknowledgments

- **CLIP** - OpenAI's vision-language model
- **FaceNet** - Google's face recognition
- **EasyOCR** - Text extraction
- **ChromaDB** - Vector database
- **FastAPI** - Modern Python web framework
- **React** - UI framework

---

## 🌟 Support

If FindMyPic helps you, give it a ⭐ on GitHub!

**Issues or questions?** Open an issue on [GitHub](https://github.com/Ryuki0x1/FindMyFile/issues)

---

**Made with ❤️ for privacy-conscious photo enthusiasts**
