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

    # Search for matching faces
    raw_results = face_store.search_face(ref_embedding, n_results=n_results)

    # Deduplicate by source file (one face per photo in results)
    seen_files = set()
    results = []
    for i, face_id in enumerate(raw_results["ids"]):
        metadata = raw_results["metadatas"][i]
        distance = raw_results["distances"][i]
        source_file = metadata.get("source_file_id", "")

        if source_file in seen_files:
            continue
        seen_files.add(source_file)

        # Cosine distance → similarity
        similarity = max(0, 1 - (distance / 2))

        results.append({
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
        })

    return {
        "query": "face_search",
        "total_results": len(results),
        "results": results,
    }
