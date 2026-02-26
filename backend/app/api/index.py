"""
Indexing API endpoints.
"""

import asyncio
from fastapi import APIRouter, Request, BackgroundTasks, HTTPException
from app.models.schemas import IndexRequest, IndexProgressResponse
from app.core.indexer import index_directory, index_directory_incremental, get_progress, cancel_indexing, scan_directory

router = APIRouter()


@router.post("/start")
async def start_indexing(
    request: Request,
    body: IndexRequest,
    background_tasks: BackgroundTasks,
):
    """
    Start indexing files in the specified paths.
    Runs as a background task — poll /api/index/progress for updates.
    """
    progress = get_progress()
    if progress.is_running:
        raise HTTPException(status_code=409, detail="Indexing already in progress")

    clip_embedder = request.app.state.clip_embedder
    vector_store = request.app.state.vector_store
    face_embedder = request.app.state.face_embedder
    face_store = request.app.state.face_store
    ocr_engine = request.app.state.ocr_engine

    # Validate paths
    valid_paths = []
    for path in body.paths:
        import os
        # Normalize the path — strip whitespace, fix separators
        path = path.strip().replace("/", "\\")
        # Bare drive letters like "E:" need trailing backslash to work with os.path.isdir
        if len(path) == 2 and path[1] == ":":
            path = path + "\\"
        # Also handle "E:" with no backslash
        if len(path) >= 2 and path[1] == ":" and not path.endswith("\\") and not os.path.exists(path):
            path = path.rstrip("\\") + "\\"

        if not os.path.exists(path):
            raise HTTPException(status_code=400, detail=f"Path not found: {path}. Make sure the drive is connected and accessible.")
        if not os.path.isdir(path):
            raise HTTPException(status_code=400, detail=f"Not a folder: {path}")
        valid_paths.append(path)

    # Start indexing for each path in background
    async def _run_indexing():
        for path in valid_paths:
            await index_directory(
                path, clip_embedder, vector_store,
                face_embedder=face_embedder,
                face_store=face_store,
                ocr_engine=ocr_engine,
            )

    # Run as a background coroutine
    asyncio.create_task(_run_indexing())

    return {
        "status": "started",
        "paths": valid_paths,
        "message": f"Indexing {len(valid_paths)} path(s). Poll /api/index/progress for updates.",
    }


@router.get("/progress", response_model=IndexProgressResponse)
async def indexing_progress():
    """Get the current indexing progress."""
    return get_progress().to_dict()


@router.post("/cancel")
async def cancel():
    """Cancel the current indexing job."""
    cancel_indexing()
    return {"status": "cancelled"}


@router.post("/scan")
async def scan_files(body: IndexRequest):
    """
    Dry-run scan — returns file count without indexing.
    Useful for showing the user how many files will be indexed.
    """
    total = 0
    breakdown = {}
    for path in body.paths:
        import os
        if os.path.isdir(path):
            files = scan_directory(path)
            total += len(files)
            breakdown[path] = len(files)

    return {
        "total_files": total,
        "breakdown": breakdown,
    }


@router.post("/incremental")
async def start_incremental_indexing(
    request: Request,
    body: IndexRequest,
    background_tasks: BackgroundTasks,
):
    """
    Start incremental indexing - only processes new, modified, or deleted files.
    Much faster than full re-indexing for large photo libraries.
    """
    progress = get_progress()
    if progress.is_running:
        raise HTTPException(status_code=409, detail="Indexing already in progress")

    clip_embedder = request.app.state.clip_embedder
    vector_store = request.app.state.vector_store
    face_embedder = request.app.state.face_embedder
    face_store = request.app.state.face_store
    ocr_engine = request.app.state.ocr_engine

    # Validate paths (same as regular indexing)
    valid_paths = []
    for path in body.paths:
        import os
        path = path.strip().replace("/", "\\")
        if len(path) == 2 and path[1] == ":":
            path = path + "\\"
        if len(path) >= 2 and path[1] == ":" and not path.endswith("\\") and not os.path.exists(path):
            path = path.rstrip("\\") + "\\"

        if not os.path.exists(path):
            raise HTTPException(status_code=400, detail=f"Path not found: {path}")
        if not os.path.isdir(path):
            raise HTTPException(status_code=400, detail=f"Not a folder: {path}")
        valid_paths.append(path)

    # Start incremental indexing for each path in background
    async def _run_incremental():
        for path in valid_paths:
            await index_directory_incremental(
                path, clip_embedder, vector_store,
                face_embedder=face_embedder,
                face_store=face_store,
                ocr_engine=ocr_engine,
            )

    # Run as a background coroutine
    asyncio.create_task(_run_incremental())

    return {
        "status": "started",
        "mode": "incremental",
        "paths": valid_paths,
        "message": f"Incremental indexing {len(valid_paths)} path(s). Only new/modified files will be processed.",
    }
