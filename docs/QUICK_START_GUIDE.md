# FindMyFile - Quick Start Guide

## 🚀 Using the New Features

### 1️⃣ Search with Minimum Score Filter

**Problem:** Getting too many unrelated results?

**Solution:** Use the `min_score` parameter to filter out low-quality matches.

```javascript
// Example API call
POST http://localhost:8000/api/search/
{
  "query": "sunset beach",
  "min_score": 70  // Only show results >= 70% relevance
}
```

**Recommended Thresholds:**
- `min_score: 60` - Balanced (default recommendation)
- `min_score: 70` - Stricter (fewer but better results)
- `min_score: 80` - Very strict (only top matches)

---

### 2️⃣ Search Specific Folder

**Problem:** Searching 10,000 files when you know it's in a specific folder?

**Solution:** Use `folder_path` to search only that folder (10x faster!).

```javascript
POST http://localhost:8000/api/search/
{
  "query": "family photo",
  "folder_path": "D:\\Photos\\2024\\Summer"
}
```

**How it works:**
- Searches the specified folder AND all subfolders
- Uses `$contains` matching, so partial paths work
- Example: "D:\\Photos" will match "D:\\Photos\\2024\\Summer\\beach.jpg"

---

### 3️⃣ Combined Filters

**Use multiple filters together for ultra-precise results:**

```javascript
POST http://localhost:8000/api/search/
{
  "query": "vacation photos",
  "folder_path": "D:\\Photos\\2024",
  "min_score": 75,
  "file_type": "image",
  "n_results": 10
}
```

**This will:**
- Search only in "D:\\Photos\\2024" folder
- Return only image files
- Show only matches >= 75% relevance
- Limit to top 10 results

---

## 📦 Building for Distribution

### Option A: CPU-Only Build (Recommended)

**Size:** 500MB (vs 8.6GB)  
**Best for:** Most users, any PC

```batch
# Step 1: Run the build script
build_cpu_only.bat

# Step 2: Test it works
cd backend
.venv-dist\Scripts\activate
python -m app.main

# Step 3: Open browser
# http://localhost:8000
```

**What you get:**
- Clean Python environment with CPU-only PyTorch
- 94% smaller than GPU version
- Works on any computer
- Good performance for <10,000 photos

---

### Option B: Create Windows Executable

**Creates a standalone .exe file:**

```batch
# Step 1: Build the executable
build_windows.bat

# Step 2: Find your app
# Location: dist\FindMyFile\FindMyFile.exe

# Step 3: Distribute
# Zip the dist\FindMyFile folder and share!
```

---

## 📊 Understanding Search Results

### Result Format:
```json
{
  "query": "sunset",
  "total_results": 5,
  "filters_applied": {
    "folder_path": "D:\\Photos",
    "min_score": 70,
    "file_type": null,
    "extension": null
  },
  "results": [
    {
      "filename": "sunset_beach.jpg",
      "relevance_score": 85.0,
      "match_type": "visual",
      "filepath": "D:\\Photos\\sunset_beach.jpg",
      "ocr_text": ""
    }
  ]
}
```

### Match Types:
- `"visual"` - Matched by image content (CLIP)
- `"text"` - Matched by OCR text
- `"visual+text"` - Matched by both (highest confidence)

---

## 🎯 How Search Works

### 1. Visual Search (CLIP)
```
Your Query: "sunset beach"
     ↓
CLIP converts to 768-dim vector
     ↓
Compare with all image vectors (cosine similarity)
     ↓
Return top matches (sorted by similarity)
```

**Why some results seem unrelated:**
- CLIP learns from 400M image-text pairs
- Sometimes matches on color, composition, or abstract concepts
- **Fix:** Use `min_score` to filter weak matches

### 2. OCR Text Search
```
Your Query: "GYM BILL"
     ↓
Search extracted OCR text (substring matching)
     ↓
Return files containing that text
     ↓
Boost score to 85% (high confidence)
```

**Why OCR sometimes fails:**
- Handwritten text
- Low contrast or blurry images
- Artistic fonts
- **Fix:** OCR already gets high scores (85%), so they appear first

### 3. Face Search
```
Your Upload: face.jpg
     ↓
Detect face + create 512-dim embedding
     ↓
Compare with all face embeddings
     ↓
Return photos with matching faces
```

**Why some faces don't match:**
- Profile views (works best with frontal faces)
- Occluded faces (sunglasses, masks)
- Very low resolution
- **Fix:** Use clear, frontal face photos as reference

---

## 🔧 Troubleshooting

### "Too many unrelated results"
**Solution:** Increase `min_score` parameter
```json
{ "query": "cat", "min_score": 75 }
```

### "Search is slow"
**Solution:** Use folder filtering
```json
{ "query": "photo", "folder_path": "D:\\Photos\\2024" }
```

### "Package is too large to share"
**Solution:** Use CPU-only build
```batch
build_cpu_only.bat
```

### "No faces detected"
**Check:**
- Are faces visible and frontal?
- Is image resolution good enough?
- Try re-indexing with face detection enabled

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `IMPROVEMENTS_SUMMARY.md` | Complete technical details of all improvements |
| `DEPLOYMENT.md` | Full deployment guide with all strategies |
| `QUICK_START_GUIDE.md` | This file - quick reference |
| `PROGRESS.md` | Project progress tracker |
| `PRD.md` | Product requirements document |

---

## 💡 Pro Tips

### Tip 1: Start Broad, Then Filter
```javascript
// First search: Get overview
{ "query": "vacation" }

// Then narrow down:
{ "query": "vacation", "folder_path": "D:\\Photos\\2024", "min_score": 70 }
```

### Tip 2: Use Specific Queries
```javascript
// Vague:
{ "query": "photo" }  // Too generic

// Better:
{ "query": "beach sunset with palm trees" }  // More specific
```

### Tip 3: Combine with File Type
```javascript
{
  "query": "receipt",
  "file_type": "image",
  "min_score": 80  // High confidence for receipts
}
```

### Tip 4: Folder Organization Matters
Organize photos by date/event for faster searching:
```
D:\Photos\
  ├── 2024\
  │   ├── Summer_Vacation\
  │   ├── Birthday_Party\
  │   └── Work_Events\
  └── 2023\
      └── ...
```

Then search specific events:
```json
{ "query": "group photo", "folder_path": "D:\\Photos\\2024\\Birthday_Party" }
```

---

## 🎬 Next Steps

1. ✅ **Read this guide**
2. 🧪 **Test new search features** with `min_score` and `folder_path`
3. 📦 **Try CPU-only build** with `build_cpu_only.bat`
4. 🚀 **Create executable** with `build_windows.bat`
5. 📖 **Read** `DEPLOYMENT.md` for publishing

---

## ❓ Questions?

Check these files for more info:
- Technical details → `IMPROVEMENTS_SUMMARY.md`
- Deployment help → `DEPLOYMENT.md`
- Feature status → `PROGRESS.md`

---

**Made with ❤️ by Rovo Dev**
