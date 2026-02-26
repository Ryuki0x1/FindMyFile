"""
Settings API endpoints.
"""

import json
import os
from fastapi import APIRouter, Request
from app.models.schemas import SettingsResponse, GPUInfoResponse
from app.core.config import get_settings
from app.ai.gpu_detect import get_system_info

router = APIRouter()


@router.get("/")
async def get_current_settings(request: Request):
    """Get current application settings."""
    settings = get_settings()
    vector_store = request.app.state.vector_store

    # Load indexed folders from config
    indexed_folders = []
    if os.path.exists(settings.config_file):
        try:
            with open(settings.config_file, "r") as f:
                config = json.load(f)
                indexed_folders = config.get("indexed_folders", [])
        except (json.JSONDecodeError, IOError):
            pass

    return {
        "indexed_folders": indexed_folders,
        "total_indexed_files": vector_store.count(),
        "excluded_folders": settings.excluded_folders,
        "image_extensions": settings.image_extensions,
        "document_extensions": settings.document_extensions,
        "video_extensions_excluded": settings.video_extensions,
        "batch_size": settings.batch_size,
        "max_file_size_mb": settings.max_file_size_mb,
        "data_dir": settings.data_dir,
        "chroma_dir": settings.chroma_dir,
        "thumbnails_dir": settings.thumbnails_dir,
    }


@router.get("/system-info")
async def system_info():
    """Get GPU, RAM, and model tier recommendation."""
    info = get_system_info()
    return info


@router.post("/clear-index")
async def clear_index(request: Request):
    """Clear ALL indexed data (images + faces). This is destructive!"""
    vector_store = request.app.state.vector_store
    face_store = request.app.state.face_store
    vector_store.clear()
    face_store.clear()
    return {"status": "cleared", "message": "All indexed data has been removed."}


@router.post("/save-folders")
async def save_indexed_folders(request: Request, folders: list[str]):
    """Save the list of folders the user has chosen to index."""
    settings = get_settings()
    os.makedirs(os.path.dirname(settings.config_file), exist_ok=True)

    config = {}
    if os.path.exists(settings.config_file):
        try:
            with open(settings.config_file, "r") as f:
                config = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

    config["indexed_folders"] = folders

    with open(settings.config_file, "w") as f:
        json.dump(config, f, indent=2)

    return {"status": "saved", "folders": folders}
