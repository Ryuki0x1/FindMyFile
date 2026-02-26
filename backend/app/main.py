"""
FindMyPic — FastAPI Backend Entry Point
Starts the API server on http://localhost:8000
"""

import os
import sys
import mimetypes
from contextlib import asynccontextmanager
from urllib.parse import unquote

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

# Ensure the backend package is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.api import search, index, settings
from app.core.config import get_settings
from app.core.first_run import get_or_create_config
from app.db.vector_store import VectorStore, FaceStore
from app.ai.clip_embed import CLIPEmbedder
from app.ai.text_embed import TextEmbedder
from app.ai.face_embed import FaceEmbedder
from app.ai.ocr_engine import OCREngine


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Startup and shutdown logic."""
    cfg = get_settings()

    # Ensure data directories exist
    os.makedirs(cfg.data_dir, exist_ok=True)
    os.makedirs(cfg.chroma_dir, exist_ok=True)
    os.makedirs(cfg.thumbnails_dir, exist_ok=True)
    
    # Run first-time setup wizard (detects GPU, creates optimized config)
    user_config = get_or_create_config()
    application.state.user_config = user_config

    # Initialize shared resources
    print("[FindMyPic] Initializing vector store...")
    application.state.vector_store = VectorStore(persist_dir=cfg.chroma_dir)

    print("[FindMyPic] Initializing face store...")
    application.state.face_store = FaceStore(persist_dir=cfg.chroma_dir)

    print("[FindMyPic] Loading CLIP model...")
    application.state.clip_embedder = CLIPEmbedder()

    print("[FindMyPic] Loading text embedder...")
    application.state.text_embedder = TextEmbedder()

    print("[FindMyPic] Loading face embedder...")
    application.state.face_embedder = FaceEmbedder()

    print("[FindMyPic] Loading OCR engine...")
    application.state.ocr_engine = OCREngine()

    print(f"[FindMyPic] Ready! API at http://localhost:{cfg.port}")
    yield

    # Shutdown
    print("[FindMyPic] Shutting down...")


app = FastAPI(
    title="FindMyPic API",
    description="Local AI-powered photo & document search engine",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS — allow frontend on any localhost port
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routes
app.include_router(search.router, prefix="/api/search", tags=["Search"])
app.include_router(index.router, prefix="/api/index", tags=["Indexing"])
app.include_router(settings.router, prefix="/api/settings", tags=["Settings"])

# Serve thumbnails as static files
_cfg = get_settings()
os.makedirs(_cfg.thumbnails_dir, exist_ok=True)
app.mount("/thumbnails", StaticFiles(directory=_cfg.thumbnails_dir), name="thumbnails")


@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "ok", "service": "FindMyPic", "version": "0.1.0"}


@app.get("/api/file", tags=["Files"])
async def serve_local_file(path: str = Query(..., description="Absolute file path to serve")):
    """
    Serve a local file by its absolute path.
    This lets the web frontend display images that live on disk
    without relying on the file:// protocol (which browsers block).
    """
    filepath = unquote(path)
    if not os.path.isfile(filepath):
        raise HTTPException(status_code=404, detail="File not found")

    # Determine content type
    content_type, _ = mimetypes.guess_type(filepath)
    if not content_type:
        content_type = "application/octet-stream"

    return FileResponse(
        path=filepath,
        media_type=content_type,
        filename=os.path.basename(filepath),
    )


if __name__ == "__main__":
    cfg = get_settings()
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=cfg.port,
        reload=False,
    )
