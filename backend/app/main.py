"""
FindMyFile — FastAPI Backend Entry Point
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
    print("[FindMyFile] Loading CLIP model...")
    clip_embedder = CLIPEmbedder()
    clip_embedder.load_model()  # Load now so we know the embedding dim
    application.state.clip_embedder = clip_embedder

    print("[FindMyFile] Initializing vector store...")
    # Pass embedding dim so VectorStore can detect & fix dimension mismatches on startup
    application.state.vector_store = VectorStore(
        persist_dir=cfg.chroma_dir,
        embedding_dim=clip_embedder.embedding_dim,
    )

    print("[FindMyFile] Initializing face store...")
    application.state.face_store = FaceStore(persist_dir=cfg.chroma_dir)

    print("[FindMyFile] Loading text embedder...")
    application.state.text_embedder = TextEmbedder()

    print("[FindMyFile] Loading face embedder...")
    application.state.face_embedder = FaceEmbedder()

    print("[FindMyFile] Loading OCR engine...")
    ocr_engine = OCREngine()
    # Don't pre-load EasyOCR — it's slow and lazy-loads fine on first use
    application.state.ocr_engine = ocr_engine

    print(f"[FindMyFile] Ready! API at http://localhost:{cfg.port}")
    print(f"[FindMyFile] CLIP model: {clip_embedder.model_name} ({clip_embedder.embedding_dim}-dim)")
    yield

    # Shutdown
    print("[FindMyFile] Shutting down...")


app = FastAPI(
    title="FindMyFile API",
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
    return {"status": "ok", "service": "FindMyFile", "version": "0.1.0"}


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

    # For PDFs: don't force download — let browser render inline
    # For others: suggest filename but still allow inline display
    disposition = "inline"

    return FileResponse(
        path=filepath,
        media_type=content_type,
        filename=os.path.basename(filepath),
        headers={
            "Content-Disposition": f'{disposition}; filename="{os.path.basename(filepath)}"',
            "X-Content-Type-Options": "nosniff",
            # Allow embedding in our own frontend iframe
            "Access-Control-Allow-Origin": "*",
        },
    )


if __name__ == "__main__":
    cfg = get_settings()
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=cfg.port,
        reload=False,
    )
