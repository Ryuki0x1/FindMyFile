# 🤖 AGENTS.md — Rovo Dev Session Context for FindMyFile

> **For any AI agent starting a new session:** Read this file FIRST before doing anything.
> This file preserves project context across sessions and login changes.
> Last updated: 2026-02-28

---

## 🎯 Project Overview

**FindMyFile** (also called "FindMyPic") is a **local AI-powered photo & document search engine** for Windows.
It lets users search their files using natural language (e.g. "sunset at the beach", "invoice from January").

### Core Concept
- No cloud. Everything runs **100% locally** on the user's machine.
- AI models run on GPU (if available) or CPU fallback.
- Users point it at a folder → it indexes everything → they search with natural language.

---

## 🧱 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python + FastAPI + Uvicorn |
| Frontend | React + TypeScript + Vite |
| AI - Visual Search | CLIP (OpenAI's model via HuggingFace) |
| AI - Text Search | Sentence Transformers (text embedder) |
| AI - Face Search | Face detection + embedding model |
| AI - OCR | OCR engine for text-in-image search |
| Vector DB | ChromaDB (local, persistent) |
| Settings | Pydantic Settings + `.env` / env vars |

---

## 📁 Project Structure

```
FindMyFile/
├── AGENTS.md               ← YOU ARE HERE (context file for AI agents)
├── README.md               ← Consumer-facing user guide
├── SETUP.bat               ← One-click setup wizard (installs deps)
├── start.bat               ← App launcher
├── PROJECT_STRUCTURE.md    ← Detailed structure doc
│
├── backend/
│   ├── requirements.txt          GPU version
│   ├── requirements-runtime.txt  CPU version
│   ├── requirements-dev.txt      Dev dependencies
│   └── app/
│       ├── main.py               FastAPI app entry point (port 8000)
│       ├── api/
│       │   ├── search.py         Search endpoints (visual, OCR, face)
│       │   ├── index.py          Indexing endpoints
│       │   └── settings.py       Settings endpoints
│       ├── ai/
│       │   ├── clip_embed.py     CLIP visual embedder
│       │   ├── text_embed.py     Text/sentence embedder
│       │   ├── face_embed.py     Face detection + embedding
│       │   ├── ocr_engine.py     OCR for text-in-image
│       │   └── gpu_detect.py     GPU detection utility
│       ├── core/
│       │   ├── config.py         App settings (pydantic-settings)
│       │   ├── indexer.py        File indexing logic
│       │   ├── searcher.py       Search logic (CLIP + OCR merge)
│       │   ├── metadata.py       File metadata extraction
│       │   └── first_run.py      First-time setup wizard
│       └── db/
│           └── vector_store.py   ChromaDB wrapper (VectorStore + FaceStore)
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx               Main app + routing + health check
│   │   ├── pages/
│   │   │   ├── SearchPage.tsx    Main search UI
│   │   │   ├── IndexingPage.tsx  Indexing dashboard UI
│   │   │   └── SettingsPage.tsx  Settings UI
│   │   ├── components/
│   │   │   ├── SearchBar.tsx     Search input component
│   │   │   ├── ResultsGrid.tsx   Search results grid
│   │   │   ├── FaceSearch.tsx    Face search upload component
│   │   │   ├── FilePreview.tsx   File preview modal
│   │   │   ├── Navbar.tsx        Navigation bar
│   │   │   ├── Onboarding.tsx    First-run onboarding wizard
│   │   │   ├── SearchFilters.tsx Filter controls
│   │   │   └── IndexingDashboard.tsx Indexing progress/stats
│   │   └── services/
│   │       └── api.ts            All API calls to backend
│   └── vite.config.ts            Frontend build config
│
└── test_images/                  Sample test images (8 images)
    └── [blue_ocean, city_skyline, green_forest, etc.]
```

---

## ⚙️ Key Configuration

- **Backend port:** `8000` (configurable via `FindMyFile_PORT` env var)
- **Data dir:** `<project_root>/data/` (configurable via `FindMyFile_DATA_DIR`)
  - `data/chroma_db/` — vector database
  - `data/thumbnails/` — cached thumbnails
  - `data/config.json` — user settings
- **AI models cached at:** `~/.cache/huggingface/` (~750MB)
- **Env prefix:** `FindMyFile_` (e.g. `FindMyFile_PORT=8080`)

---

## 🔍 How Search Works

1. **CLIP visual search** — converts query text to embedding, searches ChromaDB for similar images
2. **OCR text search** — searches for exact text found inside images (via `vector_store.text_search()`)
3. **Results merged** — deduped, scored, sorted by `relevance_score` (0-100)
4. **Face search** — separate endpoint, upload a reference face image → finds matching people in photos

**Similarity scoring:**
```python
similarity = max(0, 1 - (distance / 2))  # cosine distance → 0-1
# Boosted if > 0.8, position penalty applied, capped at 100
```

---

## ✅ Current State / What's Done

- [x] Full FastAPI backend with lifespan startup (loads all AI models)
- [x] CLIP visual search working
- [x] OCR text-in-image search working
- [x] Face detection + search working
- [x] ChromaDB vector store (persistent)
- [x] React frontend with routing (Search, Indexing, Settings pages)
- [x] Onboarding wizard for first-run
- [x] Health check + backend status indicator
- [x] File serving endpoint (`/api/file?path=...`)
- [x] Thumbnail serving (`/thumbnails/`)
- [x] CORS configured for local dev
- [x] GPU auto-detection
- [x] SETUP.bat and start.bat for Windows users
- [x] Consumer-ready README and project structure

## ⏳ What's Pending / TODO

- [ ] Test on clean Windows VM
- [ ] Create GitHub release / zip distribution
- [ ] Update version numbers for release
- [ ] `docs/` folder referenced in PROJECT_STRUCTURE.md but not present in repo

---

## 🚀 How to Run (Dev)

**Backend:**
```bash
cd backend
.venv\Scripts\python.exe -m app.main
# API available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

**Frontend:**
```bash
cd frontend
npm run dev
# UI available at http://localhost:5173
```

**First time setup:**
```
SETUP.bat   ← run this once
start.bat   ← run this every time
```

---

## 🧑‍💻 Developer Notes

- The `get_settings()` function uses `@lru_cache()` — call `get_settings.cache_clear()` if you change env vars at runtime
- `VectorStore` and `FaceStore` are both in `backend/app/db/vector_store.py`
- All AI models are loaded at startup in `main.py` `lifespan()` and attached to `app.state`
- API routes access shared models via `request.app.state.<model>`
- Frontend uses `localStorage.getItem("FindMyFile_setup_done")` to track onboarding

---

## 📋 Session Handoff Notes

> **Add notes here whenever you finish a session so the next session picks up cleanly.**

### Session: 2026-02-28 (Bug Fix Session)
**Problems solved:**
1. **Search only returned 20 results max** — fixed by:
   - Raising default `n_results` from 20 → 50 in `searcher.py`, `schemas.py`
   - Raising max cap from 100 → 500 in `schemas.py`
   - Fixed empty-collection crash in `vector_store.py` (`count() or 1` → proper early return)
   - Added "Show up to: 20/50/100/200" dropdown in the search UI (`SearchBar.tsx`)

2. **Documents (PDFs, DOCX, TXT) were never actually indexed** — fixed in `indexer.py`:
   - Documents now get indexed using CLIP text embedding of filename + extracted text
   - Plain text files (`.txt`, `.md`, `.csv`) are read directly
   - OCR engine used for scanned PDFs

3. **Batch embedding bug** — fixed indexer to properly separate image vs document entries using index lists, fixing a bug where document None placeholders would break the CLIP batch embedder

4. **Incremental indexing not exposed in frontend** — fixed:
   - Added `startIncrementalIndexing()` to `api.ts`
   - IndexingPage now has two buttons: ⚡ Update Index (incremental, default) and 🔄 Full Re-Index

**Files changed:**
- `backend/app/models/schemas.py` — n_results default 20→50, max 100→500
- `backend/app/core/searcher.py` — n_results default 20→50
- `backend/app/db/vector_store.py` — fixed empty collection crash in search
- `backend/app/core/indexer.py` — document indexing support, batch fix
- `frontend/src/services/api.ts` — added `startIncrementalIndexing()`
- `frontend/src/pages/IndexingPage.tsx` — ⚡ Update Index / 🔄 Full Re-Index buttons
- `frontend/src/components/SearchBar.tsx` — n_results selector (20/50/100/200)
- `frontend/src/components/SearchBar.css` — styles for n_results selector

**Still pending:**
- [ ] Test on clean Windows VM
- [ ] Create GitHub release / zip distribution
- [ ] `docs/` folder referenced in PROJECT_STRUCTURE.md but not present in repo
- [ ] Run `pip install PyMuPDF python-docx python-pptx openpyxl` in venv after pulling

### Session: 2026-02-28 (Search Quality + Face + OCR Improvements)
**Improvements made:**

1. **Face search improved** (`face_embed.py`, `search.py`):
   - MTCNN detector: margin 20→30, thresholds relaxed [0.6,0.7,0.7], detects smaller faces (min 30px)
   - Confidence threshold lowered 0.90→0.85 (catches more valid faces)
   - Added tiny face filter (<20px) to remove false positives
   - Face search now fetches 5× more candidates and keeps BEST match per file (not just first seen)
   - Added 50% similarity floor — only real matches returned
   - Results sorted by best face similarity score

2. **OCR massively improved** (`ocr_engine.py`):
   - Now uses **native text extraction** for digital files (no OCR needed):
     - PDF → PyMuPDF (`fitz`) — instant, perfect text from digital PDFs
     - DOCX → python-docx — full paragraph + table extraction
     - PPTX → python-pptx — all slide text shapes
     - XLSX/CSV → openpyxl — cell value extraction
     - TXT/MD/RTF → direct read (10KB)
   - Scanned PDFs: renders pages as 2× zoom images, then EasyOCR
   - EasyOCR now uses `detail=1` with confidence filtering (≥0.4) — removes garbage text
   - Small images upscaled 1.5× before OCR for better accuracy
   - `paragraph=False` — keeps individual words for better keyword matching

3. **Search scoring massively improved** (`searcher.py`):
   - New `_keyword_score()` function: exact phrase > whole word > substring > partial
   - New `_filename_score()` function: matches query words in filenames
   - CLIP fetches 3× more candidates then re-ranks with keyword signals
   - Keyword hit in OCR text = major score boost (overrides low CLIP score)
   - Filename keyword match = secondary boost
   - Text-only results scored 70–95 based on keyword quality (not fixed 85)
   - `match_type` correctly reflects visual / text / visual+text

4. **Document indexing improved** (`indexer.py`):
   - Uses OCR engine's smart extractor (handles all formats natively)
   - Stores 2000 chars of text (was 1000) for better keyword coverage
   - CLIP embed text uses first 400 chars of content (was 200)

5. **New packages required** (`requirements.txt`, `requirements-runtime.txt`):
   - `PyMuPDF` — PDF native text extraction
   - `python-docx` — DOCX extraction
   - `python-pptx` — PPTX extraction
   - `openpyxl` — XLSX extraction
   - Install: `pip install PyMuPDF python-docx python-pptx openpyxl`

**Files changed:**
- `backend/app/ai/face_embed.py`
- `backend/app/ai/ocr_engine.py`
- `backend/app/core/searcher.py`
- `backend/app/core/indexer.py`
- `backend/app/api/search.py`
- `backend/requirements.txt`
- `backend/requirements-runtime.txt`

**⚠️ IMPORTANT: After pulling these changes, run:**
```
cd backend
.venv\Scripts\pip.exe install PyMuPDF python-docx python-pptx openpyxl
```
**Then do a Full Re-Index** so documents get re-processed with the new extractors.

### Session: 2026-02-28 (Indexing Fix + Dimension Mismatch Auto-Repair)
**Problems solved:**
- Indexing completely broken after CLIP model upgrade (embedding dimension mismatch)
- ChromaDB silently rejects embeddings with wrong dimensions, causing 0 files indexed

**Fixes:**
1. **VectorStore auto-detects dimension mismatch** (`vector_store.py`):
   - On startup, checks stored embedding dim vs current model dim
   - If mismatch detected → automatically clears collection and prints warning
   - User just needs to restart backend + run Full Re-Index

2. **main.py loads CLIP first** so embedding_dim is known before VectorStore init
   - Passes `embedding_dim` to `VectorStore.__init__()` for mismatch detection
   - Prints active model name + dim at startup

3. **Better indexer error logging** (`indexer.py`):
   - Validates embedding shape before storing
   - Prints per-batch success: "Batch done: N images embedded (768-dim)"
   - Clear ❌ error messages with full traceback on failure

**Files changed:**
- `backend/app/db/vector_store.py` — dimension mismatch detection + auto-clear
- `backend/app/main.py` — load CLIP first, pass dim to VectorStore
- `backend/app/core/indexer.py` — better error logging

**⚠️ To fix indexing:**
1. Restart backend — it will auto-detect the mismatch and clear old data
2. Run **🔄 Full Re-Index** in the UI

### Session: 2026-02-28 (Model Upgrades + FaceSearch UI Fix)
**Improvements made:**

1. **CLIP model auto-upgraded** (`clip_embed.py`):
   - Detects GPU VRAM at startup and picks the best available model:
     - ≥6GB VRAM → `openai/clip-vit-large-patch14` (best quality, 768-dim)
     - ≥3GB VRAM → `openai/clip-vit-base-patch16` (good quality)
     - <3GB VRAM → `openai/clip-vit-base-patch32` (fast, smallest)
     - CPU → `openai/clip-vit-base-patch16` (better than base-32)
   - ViT-L/14 is ~40% better at semantic search than ViT-B/32
   - ⚠️ Requires Full Re-Index after upgrade (different embedding dimensions)

2. **Text embedder upgraded** (`text_embed.py`):
   - Changed from `all-MiniLM-L6-v2` (384-dim) → `all-mpnet-base-v2` (768-dim)
   - Much better semantic understanding for document and OCR text search
   - ⚠️ Requires Full Re-Index after upgrade

3. **FaceSearch folder scope UI completely redesigned** (`FaceSearch.tsx`, `FaceSearch.css`):
   - Consistent themed design with control-header / value pattern
   - Folder scope selector properly separated with divider line
   - "Change Photo" + "Clear" action buttons at the bottom
   - No more glitchy layout — fully responsive

**Files changed:**
- `backend/app/ai/clip_embed.py`
- `backend/app/ai/text_embed.py`
- `frontend/src/components/FaceSearch.tsx`
- `frontend/src/components/FaceSearch.css`

**⚠️ IMPORTANT: After pulling, do a Full Re-Index** — embedding dimensions changed!

### Session: 2026-02-28 (Face Folder Scope + Browse Removed)
**Changes:**
1. **Face search folder scope** — face search now has same folder scope picker as text search
   - `FaceSearch.tsx` — folder dropdown loaded from `/api/search/folders`, re-runs search on change
   - `search.py` — `folder_path` param added to `/api/search/face` endpoint, filters results by filepath
   - `api.ts` — `faceSearch()` now accepts `folderPath` param
   - CSS added to `FaceSearch.css`

2. **Browse feature removed** — removed `/browse` page, navbar link, route, and backend endpoint
   - Deleted `BrowsePage.tsx`, `BrowsePage.css`
   - Removed route from `App.tsx`, link from `Navbar.tsx`
   - Removed `/browse` GET endpoint from `search.py`
   - Removed `browseFiles()` + `BrowseResponse` from `api.ts`

### Session: 2026-02-28 (All Results + Folder Scope Picker)
**Features added:**
1. **"All results" option in search** — n_results now supports 500 and "All results" (9999) options
   - Schema max raised from 500 → 9999
   - Searcher and vector_store handle large result sets properly
   - Frontend dropdown: 20 / 50 / 100 / 200 / 500 / All results

2. **Folder Scope Picker** (`SearchFilters.tsx`, `search.py`, `api.ts`):
   - New `/api/search/folders` endpoint — returns all unique folders that have indexed files
   - Filters panel now shows a **dropdown of all your indexed folders** instead of a text box
   - Select any folder → search is scoped to only that folder's files
   - ✕ button to clear the folder filter
   - Falls back to text input if no folders loaded yet

**Files changed:**
- `backend/app/api/search.py` — added `/folders` endpoint
- `backend/app/models/schemas.py` — n_results max 500→9999
- `backend/app/db/vector_store.py` — handle large n_results
- `backend/app/core/searcher.py` — handle n_results=9999 (all)
- `frontend/src/services/api.ts` — added `getIndexedFolders()`
- `frontend/src/components/SearchFilters.tsx` — folder scope dropdown
- `frontend/src/components/SearchFilters.css` — folder picker styles
- `frontend/src/components/SearchBar.tsx` — 500/All options in dropdown

### Session: 2026-02-28 (PDF Preview + FilePreview Overhaul)
**Problems solved:**
- PDFs showed a grey placeholder instead of actual content

**Improvements made:**
1. **FilePreview completely rebuilt** (`FilePreview.tsx`, `FilePreview.css`):
   - **PDF → embedded iframe** using browser's built-in PDF viewer (full scroll/zoom)
   - **TXT/MD/CSV → embedded iframe** as plain text
   - **DOCX/PPTX/XLSX → shows extracted OCR text** in a scrollable pre block
   - Wide modal layout for embeddable docs: PDF on left, metadata sidebar on right
   - File type icons per extension (📄 PDF, 📝 DOCX, 📊 PPTX, 📋 XLSX, 🗒️ TXT)
   - **🔗 Open File** button opens file in new browser tab
   - **Copy Path / Copy Folder** buttons with ✅ confirmation flash
   - Responsive: stacks vertically on small screens

2. **Backend file server improved** (`main.py`):
   - Added `Content-Disposition: inline` header — prevents forced download
   - Added `Access-Control-Allow-Origin: *` for iframe embedding
   - PDFs now render in browser instead of downloading

**Files changed:**
- `frontend/src/components/FilePreview.tsx`
- `frontend/src/components/FilePreview.css`
- `backend/app/main.py`

### Session: 2026-02-28 (UI Polish + Text-Only Mode)
**Features added:**

1. **Face search confidence slider** (`FaceSearch.tsx`, `FaceSearch.css`, `search.py`, `api.ts`):
   - Slider with range 20–90%, labeled Loose / Balanced / Strict
   - Re-runs search automatically when slider moves
   - `min_similarity` query param passed to backend `/api/search/face`
   - Backend uses the user-specified threshold instead of hardcoded 0.50

2. **OCR text highlighting** (`ResultsGrid.tsx`, `ResultsGrid.css`):
   - Query keywords highlighted in yellow in the OCR text snippet under each result
   - `HighlightedText` component uses regex for case-insensitive matching

3. **Text-only search mode** (`SearchBar.tsx`, `SearchBar.css`, `searcher.py`, `schemas.py`, `api.ts`):
   - Checkbox "📝 Text only" next to results count selector
   - When enabled, CLIP visual search is skipped — only OCR/document text searched
   - Great for finding specific words in photos or documents

4. **SETUP.bat updated** — auto-installs `PyMuPDF python-docx python-pptx openpyxl`

**Files changed:**
- `frontend/src/components/FaceSearch.tsx` + `FaceSearch.css`
- `frontend/src/components/ResultsGrid.tsx` + `ResultsGrid.css`
- `frontend/src/components/SearchBar.tsx` + `SearchBar.css`
- `frontend/src/services/api.ts`
- `backend/app/api/search.py`
- `backend/app/core/searcher.py`
- `backend/app/models/schemas.py`
- `SETUP.bat`

### Session: 2026-02-28 (Browse + Pagination Session)
**Features added:**
1. **Browse All Files page** (`/browse`) — new page to see all indexed files without searching:
   - Filter by file type (image/document) and extension
   - Sort by date modified, filename, size, or file type (asc/desc)
   - Configurable page size (25/50/100 per page)
   - Grid and list view modes
   - Skeleton loading animation
   - Click any file to open FilePreview modal

2. **Pagination on Browse page** — smart paginator with ellipsis for large libraries

3. **Pagination on Search Results** — `ResultsGrid` now paginates at 50 results per page with page controls

4. **Backend `/api/search/browse` endpoint** — GET endpoint with `page`, `page_size`, `file_type`, `extension`, `sort_by`, `sort_order` query params

5. **Navbar updated** — 🗂️ Browse link added between Search and Indexing

**Files added:**
- `frontend/src/pages/BrowsePage.tsx`
- `frontend/src/pages/BrowsePage.css`

**Files changed:**
- `backend/app/api/search.py` — added `/browse` GET endpoint
- `frontend/src/services/api.ts` — added `browseFiles()`, `BrowseResponse` type
- `frontend/src/components/Navbar.tsx` — added Browse nav link
- `frontend/src/App.tsx` — added `/browse` route + `BrowsePage` import
- `frontend/src/components/ResultsGrid.tsx` — added pagination (50/page)
- `frontend/src/components/ResultsGrid.css` — pagination styles

**Still pending:**
- [ ] Test on clean Windows VM
- [ ] Create GitHub release / zip distribution
- [ ] `docs/` folder referenced in PROJECT_STRUCTURE.md but not present in repo

### Session: 2026-02-28 (Initial)
- Project is near distribution-ready (v1.0.0)
- Main pending items: Windows VM testing, GitHub release packaging
- `docs/` folder referenced in PROJECT_STRUCTURE.md doesn't exist yet — needs to be created or reference removed
- No known bugs at time of this session

---

## 💡 Tips for the Next Agent Session

1. **Always read this file first** before making changes
2. **Update the "Session Handoff Notes" section** at the end of every session
3. **Check `PROJECT_STRUCTURE.md`** for the intended folder layout
4. **The backend models take ~30s to load** — don't assume it's broken if the health check fails immediately
5. **ChromaDB data persists** in `data/chroma_db/` — don't delete this folder accidentally
