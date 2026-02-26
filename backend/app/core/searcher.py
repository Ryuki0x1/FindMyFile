"""
Search engine — converts natural language queries to embeddings
and performs similarity search against the vector database.
Also searches OCR text stored in metadata for exact text matches.
"""

from typing import Optional
from app.ai.clip_embed import CLIPEmbedder
from app.db.vector_store import VectorStore


def search_files(
    query: str,
    clip_embedder: CLIPEmbedder,
    vector_store: VectorStore,
    n_results: int = 20,
    file_type: Optional[str] = None,
    extension: Optional[str] = None,
    folder_path: Optional[str] = None,
    min_score: Optional[float] = None,
) -> dict:
    """
    Search indexed files using natural language.
    Combines:
      1. CLIP visual similarity search (understands image content)
      2. OCR text search (finds exact text in images)

    Results from both are merged and deduplicated.
    """
    results_map = {}  # file_id -> result dict (for dedup)

    # --- 1. CLIP semantic search ---
    query_embedding = clip_embedder.embed_text(query)

    # Build filters
    where = None
    if file_type or extension or folder_path:
        conditions = []
        if file_type:
            conditions.append({"file_type": file_type})
        if extension:
            conditions.append({"extension": extension})
        if folder_path:
            # Support both exact folder and subfolder matching
            conditions.append({"folder_path": {"$contains": folder_path}})

        if len(conditions) == 1:
            where = conditions[0]
        else:
            where = {"$and": conditions}

    raw_results = vector_store.search(
        query_embedding=query_embedding,
        n_results=n_results,
        where=where,
    )

    for i, file_id in enumerate(raw_results["ids"]):
        metadata = raw_results["metadatas"][i]
        distance = raw_results["distances"][i]

        # Improved similarity calculation
        # Distance is typically 0-2 for cosine distance
        # Convert to percentage with better scaling
        similarity = max(0, 1 - (distance / 2))
        
        # Boost score slightly for very close matches
        if similarity > 0.8:
            similarity = 0.8 + (similarity - 0.8) * 1.5  # Boost top matches
        
        # Apply position penalty (later results get slight penalty)
        position_penalty = 1 - (i * 0.01)  # Max 1% penalty per position
        similarity = similarity * position_penalty

        results_map[file_id] = {
            "file_id": file_id,
            "filepath": metadata.get("filepath", ""),
            "filename": metadata.get("filename", ""),
            "extension": metadata.get("extension", ""),
            "file_type": metadata.get("file_type", ""),
            "size_mb": metadata.get("size_mb", 0),
            "created": metadata.get("created", ""),
            "modified": metadata.get("modified", ""),
            "relevance_score": round(min(similarity * 100, 100), 1),  # Cap at 100
            "date_taken": metadata.get("date_taken", ""),
            "camera_model": metadata.get("camera_model", ""),
            "ocr_text": metadata.get("ocr_text", ""),
            "match_type": "visual",
        }

    # --- 2. OCR text search (exact text in images) ---
    try:
        ocr_results = vector_store.text_search(query, n_results=n_results)
        for i, file_id in enumerate(ocr_results["ids"]):
            metadata = ocr_results["metadatas"][i]

            if file_id in results_map:
                # Already in results via CLIP — boost score and mark as text match too
                existing = results_map[file_id]
                existing["relevance_score"] = min(100, existing["relevance_score"] + 25)
                existing["match_type"] = "visual+text"
            else:
                # New result from OCR only
                results_map[file_id] = {
                    "file_id": file_id,
                    "filepath": metadata.get("filepath", ""),
                    "filename": metadata.get("filename", ""),
                    "extension": metadata.get("extension", ""),
                    "file_type": metadata.get("file_type", ""),
                    "size_mb": metadata.get("size_mb", 0),
                    "created": metadata.get("created", ""),
                    "modified": metadata.get("modified", ""),
                    "relevance_score": 85.0,  # High score for exact text match
                    "date_taken": metadata.get("date_taken", ""),
                    "camera_model": metadata.get("camera_model", ""),
                    "ocr_text": metadata.get("ocr_text", ""),
                    "match_type": "text",
                }
    except Exception:
        pass  # OCR search failure shouldn't break visual search

    # Sort by relevance (highest first)
    results = sorted(results_map.values(), key=lambda x: x["relevance_score"], reverse=True)

    # Apply minimum score filter if specified
    if min_score is not None:
        results = [r for r in results if r["relevance_score"] >= min_score]

    return {
        "query": query,
        "total_results": len(results),
        "results": results[:n_results],
        "filters_applied": {
            "file_type": file_type,
            "extension": extension,
            "folder_path": folder_path,
            "min_score": min_score,
        },
    }
