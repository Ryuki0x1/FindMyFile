# FindMyPic - User Guide

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+** - [Download](https://python.org/downloads/) *(Check "Add to PATH")*
- **Node.js 18+** - [Download](https://nodejs.org/)
- 8GB+ RAM (16GB for GPU version)

### Installation (10-15 minutes)

```bash
git clone https://github.com/Ryuki0x1/FindMyFile.git
cd FindMyFile
SETUP.bat
```

**What happens:**
1. ✅ Checks Python & Node.js
2. ✅ Detects GPU (offers CPU/GPU choice)
3. ✅ Installs dependencies
4. ✅ Downloads AI models (~540-850MB, one-time)
5. ✅ Offers to launch app

### Launch

```bash
start.bat
```

Browser opens automatically to http://localhost:5173 ✨

---

## 📖 Using FindMyPic

### 1. Index Your Photos

**First time:**
1. Click Settings (⚙️ icon)
2. Add folders containing photos
3. Click "Start Indexing"
4. Wait for completion (~1-2 sec/image on CPU, ~0.3 sec on GPU)

**Example:** 1,000 photos = 15-30 min (CPU) or 5-8 min (GPU)

### 2. Search

**Visual Search:**
```
"sunset at the beach"
"red car parked outside"
"my dog playing in the park"
```

**Face Search:**
1. Click "Face Search" tab
2. Upload reference photo
3. FindMyPic finds all photos of that person

**Text Search (OCR):**
```
"birthday card"
"restaurant menu"
"street signs"
```

### 3. Filter Results

- **Min Score:** Slide to filter low-relevance matches (70+ recommended)
- **Folder:** Search specific folders only
- **File Type:** JPG, PNG, etc.
- **Date Range:** Find photos from specific periods

---

## ⚙️ Settings

### Indexed Folders
- Add/remove folders to index
- Click "Reindex" after adding new photos

### Optimizations
- **Batch Size:** Auto-configured based on RAM
- **Model Info:** View your AI models

---

## 🔧 Troubleshooting

### Setup Issues

**"Python not found"**
- Install Python 3.10+ from python.org
- **Must check "Add Python to PATH"** during install
- Restart terminal, run `SETUP.bat` again

**"Node.js not found"**
- Install Node.js 18+ from nodejs.org
- Restart terminal, run `SETUP.bat` again

**"pip install errors"**
```bash
cd backend
rmdir /s /q .venv
cd ..
SETUP.bat
```

### Runtime Issues

**"Backend won't start"**
```bash
taskkill /f /im python.exe
start.bat
```

**"Frontend won't start"**
```bash
# Find and kill process on port 5173
netstat -ano | findstr :5173
taskkill /f /pid <PID>
start.bat
```

**"Models downloading slowly"**
- Normal! 750MB download, happens once
- Models cached in `~/.cache/`
- Future launches are instant

**"Search returns no results"**
- Make sure photos are indexed (Settings → Indexing)
- Try different search terms
- Adjust min score filter

**"Out of memory"**
- Close other programs
- Index smaller folders at a time
- Edit `data/config.json` - reduce `batch_size`

---

## ❓ FAQ

**Q: Does it work offline?**  
A: Yes! After setup, 100% offline.

**Q: Where are my photos?**  
A: They stay where they are. FindMyPic only reads them.

**Q: How much storage?**  
A: ~1KB per photo. 10,000 photos ≈ 10MB database.

**Q: Can I index multiple folders?**  
A: Yes! Add as many as you want.

**Q: CPU vs GPU?**  
A: SETUP.bat auto-detects and recommends. GPU is 10x faster for indexing.

**Q: Is my data private?**  
A: 100% YES. Everything runs locally. No cloud, no tracking.

**Q: Mac/Linux support?**  
A: Backend works on all platforms. Convert .bat scripts to .sh

---

## 🎯 Tips for Best Results

### Use Specific Search Terms
```
❌ "photo"          → ✅ "beach sunset with palm trees"
❌ "person"         → ✅ "group photo at restaurant"
```

### Organize Photos by Folder
```
D:\Photos\
  ├── 2024\
  │   ├── Vacation\
  │   ├── Work\
  │   └── Family\
  └── 2023\
```
Then use folder filter for faster searches!

### Adjust Min Score
- 60-70: More results, some irrelevant
- 70-80: Balanced
- 80+: Only highly relevant matches

### Face Search Tips
- Use clear, frontal face photos
- Good lighting helps
- Profile shots work but less accurate

### Re-index After Changes
If you add/remove many photos, re-index that folder to update the database.

---

## 📁 Where Data is Stored

```
FindMyPic/
├── data/
│   ├── chroma_db/        # Vector embeddings (search index)
│   ├── thumbnails/       # Generated thumbnails
│   └── config.json       # Your settings
│
└── ~/.cache/huggingface/ # AI models (downloaded once)
```

**Your original photos are NEVER moved, copied, or modified.**

---

## 🔒 Privacy

- ✅ Everything runs on your computer
- ✅ No cloud services
- ✅ No internet after setup
- ✅ No telemetry or tracking
- ✅ Open source - audit the code

**Your photos never leave your computer.**

---

## 🛠️ Technical Details

### AI Models Used
- **CLIP** (OpenAI) - Image/text understanding
- **FaceNet** (Google) - Face recognition
- **EasyOCR** - Text extraction

### How It Works
1. **Indexing:** AI creates "embeddings" (vectors) for each photo
2. **Storage:** Embeddings stored in ChromaDB
3. **Search:** Query converted to embedding, matched against stored photos
4. **Results:** Ranked by similarity (cosine similarity)

### Model Selection (Auto-detected)
| Hardware | Model Size | CLIP Model | Speed |
|----------|------------|------------|-------|
| High GPU (8GB+ VRAM) | ~850MB | Large | Fastest |
| Mid GPU (4-8GB VRAM) | ~540MB | Base | Fast |
| Low GPU (<4GB VRAM) | ~540MB | Base | Good |
| CPU Only | ~540MB | Base | Good |

---

## 📚 Additional Resources

- **[README.md](README.md)** - Project overview
- **[MODEL_DOWNLOADS.md](MODEL_DOWNLOADS.md)** - AI model details
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Code organization

---

## 🆘 Getting Help

1. Check FAQ above
2. Review troubleshooting section
3. Check error messages in terminal windows
4. Open issue on [GitHub](https://github.com/Ryuki0x1/FindMyFile/issues)

---

## 🎉 You're Ready!

1. ✅ Run `SETUP.bat`
2. ✅ Run `start.bat`
3. ✅ Index your photos
4. ✅ Start searching!

**Enjoy your AI-powered photo search!** 📸✨

---

*Last updated: February 2026*
