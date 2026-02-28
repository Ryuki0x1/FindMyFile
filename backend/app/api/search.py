"""
Search API endpoints.
Supports: visual similarity search (CLIP), OCR text search, and face search.
"""

import io
import os
from typing import Optional
from fastapi import APIRouter, Request, HTTPException, UploadFile, File
from PIL import Image

from app.models.schemas import SearchRequest, SearchResponse
from app.core.searcher import search_files

router = APIRouter()


@router.get("/folders")
async def list_indexed_folders(request: Request):
    """
    Returns a list of unique top-level folder paths that have been indexed.
    Used by the frontend to let users scope their search to a specific folder.
    """
    vector_store = request.app.state.vector_store
    try:
        raw = vector_store._collection.get(include=["metadatas"])
    except Exception:
        return {"folders": []}

    metadatas = raw.get("metadatas") or []
    seen_folders = set()

    for meta in metadatas:
        if not meta:
            continue
        filepath = meta.get("filepath", "")
        if not filepath:
            continue
        # Detect path separator
        sep = "\\" if "\\" in filepath else "/"
        folder = filepath.rsplit(sep, 1)[0] if sep in filepath else filepath
        if folder:
            seen_folders.add(folder)

    # Sort alphabetically
    folders = sorted(seen_folders)
    return {"folders": folders}


@router.post("/", response_model=SearchResponse)
async def search(request: Request, body: SearchRequest):
    """
    Search indexed files using natural language.
    Combines CLIP visual similarity + OCR text-in-image matching.
    """
    clip_embedder = request.app.state.clip_embedder
    vector_store = request.app.state.vector_store

    results = search_files(
        query=body.query,
        clip_embedder=clip_embedder,
        vector_store=vector_store,
        n_results=body.n_results,
        file_type=body.file_type,
        extension=body.extension,
        folder_path=body.folder_path,
        min_score=body.min_score,
        text_only=body.text_only,
    )
    return results


@router.get("/stats")
async def search_stats(request: Request):
    """Get index statistics."""
    vector_store = request.app.state.vector_store
    face_store = request.app.state.face_store
    stats = vector_store.get_stats()
    stats["total_faces"] = face_store.count()
    return stats


@router.post("/face")
async def face_search(
    request: Request,
    file: UploadFile = File(..., description="Reference face image"),
    n_results: int = 50,
    min_similarity: float = 0.50,
    folder_path: Optional[str] = None,
):
    """
    Search for photos containing a specific person.
    Upload a reference face image → returns all photos with matching faces.
    """
    face_embedder = request.app.state.face_embedder
    face_store = request.app.state.face_store

    # Read uploaded image
    contents = await file.read()
    try:
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

    # Extract face embedding from the reference image
    ref_embedding = face_embedder.embed_single_face(image)
    if ref_embedding is None:
        raise HTTPException(
            status_code=400,
            detail="No face detected in the uploaded image. Please upload a clear photo with a visible face."
        )

    # Search for matching faces — get more raw results to allow best-per-file selection
    raw_results = face_store.search_face(ref_embedding, n_results=n_results * 5)

    # For each source file, keep only the BEST matching face (highest similarity)
    # This gives one result per photo, showing the closest face match
    best_per_file: dict[str, dict] = {}
    for i, face_id in enumerate(raw_results["ids"]):
        metadata = raw_results["metadatas"][i]
        distance = raw_results["distances"][i]
        source_file = metadata.get("source_file_id", "")

        # Apply folder scope filter if specified
        if folder_path:
            file_path_val = metadata.get("filepath", "")
            if folder_path.lower() not in file_path_val.lower():
                continue

        # Cosine distance → similarity (0–1)
        similarity = max(0, 1 - (distance / 2))

        # Only include results above the user-specified minimum similarity threshold
        if similarity < min_similarity:
            continue

        if source_file not in best_per_file or similarity > best_per_file[source_file]["_sim"]:
            best_per_file[source_file] = {
                "_sim": similarity,
                "file_id": source_file,
                "filepath": metadata.get("filepath", ""),
                "filename": metadata.get("filename", ""),
                "relevance_score": round(similarity * 100, 1),
                "face_box": {
                    "x1": metadata.get("box_x1", 0),
                    "y1": metadata.get("box_y1", 0),
                    "x2": metadata.get("box_x2", 0),
                    "y2": metadata.get("box_y2", 0),
                },
                "confidence": metadata.get("confidence", 0),
                "extension": os.path.splitext(metadata.get("filename", ""))[1].lower(),
                "file_type": "image",
                "match_type": "face",
                "size_mb": 0,
                "created": "",
                "modified": "",
            }

    # Sort by similarity descending, remove internal key, cap at n_results
    results = sorted(best_per_file.values(), key=lambda x: x["_sim"], reverse=True)
    for r in results:
        r.pop("_sim", None)
    results = results[:n_results]

    return {
        "query": "face_search",
        "total_results": len(results),
        "results": results,
    }
