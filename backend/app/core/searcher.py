"""
Search engine — converts natural language queries to embeddings
and performs similarity search against the vector database.
Also searches OCR text stored in metadata for exact text matches.
Scores are merged intelligently: keyword hits get major boosts.
"""

import re
from typing import Optional
from app.ai.clip_embed import CLIPEmbedder
from app.db.vector_store import VectorStore


def _keyword_score(query: str, text: str) -> float:
    """
    Score how well a text matches the query keywords.
    Returns a value 0.0–1.0:
      - 1.0  = all query words found as whole words
      - 0.5  = all words found (substring match)
      - partial = fraction of words matched
    """
    if not text or not query:
        return 0.0

    query_lower = query.lower().strip()
    text_lower  = text.lower()

    # Exact full phrase match — highest priority
    if query_lower in text_lower:
        return 1.0

    # Word-level matching
    words = [w for w in re.split(r"\W+", query_lower) if len(w) >= 2]
    if not words:
        return 0.0

    whole_word_hits = 0
    substring_hits  = 0
    for word in words:
        pattern = r"\b" + re.escape(word) + r"\b"
        if re.search(pattern, text_lower):
            whole_word_hits += 1
        elif word in text_lower:
            substring_hits += 1

    total = len(words)
    if whole_word_hits == total:
        return 0.95   # All words matched as whole words
    elif whole_word_hits + substring_hits == total:
        return 0.80   # All words matched (some as substring)
    else:
        # Partial match
        matched = whole_word_hits + substring_hits * 0.6
        return max(0.0, matched / total * 0.7)


def _filename_score(query: str, filename: str) -> float:
    """Check if the query keywords appear in the filename."""
    return _keyword_score(query, filename.replace("_", " ").replace("-", " "))


def search_files(
    query: str,
    clip_embedder: CLIPEmbedder,
    vector_store: VectorStore,
    n_results: int = 50,
    file_type: Optional[str] = None,
    extension: Optional[str] = None,
    folder_path: Optional[str] = None,
    min_score: Optional[float] = None,
    text_only: bool = False,
) -> dict:
    """
    Search indexed files using natural language.
    Combines:
      1. CLIP visual/semantic similarity search
      2. Exact keyword search in OCR text (images + scanned docs)
      3. Native text keyword search (PDFs, DOCX, etc.)
      4. Filename keyword matching

    All three are merged, deduplicated, and scored intelligently.
    Keyword matches are always ranked higher than pure visual matches.
    """
    results_map = {}  # file_id -> result dict (for dedup)
    query_lower  = query.lower().strip()

    # Build ChromaDB filters (shared between CLIP and text search)
    where = None
    if file_type or extension or folder_path:
        conditions = []
        if file_type:
            conditions.append({"file_type": {"$eq": file_type}})
        if extension:
            conditions.append({"extension": {"$eq": extension}})
        if folder_path:
            conditions.append({"folder_path": {"$contains": folder_path}})
        where = conditions[0] if len(conditions) == 1 else {"$and": conditions}

    # --- 1. CLIP semantic search (skipped in text_only mode) ---
    if not text_only:
        query_embedding = clip_embedder.embed_text(query)

        # Fetch more candidates than needed — we re-rank below
        # For "All results" mode (n_results=9999), fetch everything
        fetch_n = min(n_results * 3, 9999) if n_results < 9999 else 9999
        raw_results = vector_store.search(
            query_embedding=query_embedding,
            n_results=fetch_n,
            where=where,
        )
    else:
        raw_results = {"ids": [], "metadatas": [], "distances": []}

    for i, file_id in enumerate(raw_results["ids"]):
        metadata  = raw_results["metadatas"][i]
        distance  = raw_results["distances"][i]

        # Cosine distance (0–2) → similarity (0–1)
        clip_sim = max(0.0, 1.0 - (distance / 2.0))

        # Boost very high CLIP matches
        if clip_sim > 0.80:
            clip_sim = 0.80 + (clip_sim - 0.80) * 1.5

        ocr_text  = metadata.get("ocr_text", "") or ""
        filename  = metadata.get("filename", "") or ""

        # Keyword scores
        kw_ocr  = _keyword_score(query, ocr_text)
        kw_file = _filename_score(query, filename)

        # Final score: CLIP base + keyword boosts
        # Keyword hit in OCR text is the strongest signal
        final_sim = clip_sim
        match_type = "visual"

        if kw_ocr > 0.5:
            # Strong text match — override CLIP with text score, add bonus
            final_sim  = max(clip_sim, kw_ocr) + 0.20
            match_type = "visual+text" if clip_sim > 0.3 else "text"
        elif kw_ocr > 0:
            final_sim  = clip_sim + kw_ocr * 0.15
            match_type = "visual+text"

        if kw_file > 0.5:
            final_sim  = max(final_sim, kw_file + 0.10)
            match_type = "visual+text" if "text" not in match_type else match_type

        results_map[file_id] = {
            "file_id":        file_id,
            "filepath":       metadata.get("filepath", ""),
            "filename":       filename,
            "extension":      metadata.get("extension", ""),
            "file_type":      metadata.get("file_type", ""),
            "size_mb":        metadata.get("size_mb", 0),
            "created":        metadata.get("created", ""),
            "modified":       metadata.get("modified", ""),
            "relevance_score": round(min(final_sim * 100, 100), 1),
            "date_taken":     metadata.get("date_taken", ""),
            "camera_model":   metadata.get("camera_model", ""),
            "ocr_text":       ocr_text,
            "match_type":     match_type,
        }

    # --- 2. Full text search in OCR/document metadata ---
    # This catches files that scored low on CLIP but have exact keyword matches
    try:
        text_results = vector_store.text_search(query, n_results=n_results)
        for i, file_id in enumerate(text_results["ids"]):
            metadata = text_results["metadatas"][i]
            ocr_text = metadata.get("ocr_text", "") or ""
            filename = metadata.get("filename", "") or ""

            kw_score = _keyword_score(query, ocr_text)
            kw_file  = _filename_score(query, filename)
            best_kw  = max(kw_score, kw_file)

            # Score for text-only matches: based on how well keywords match
            text_relevance = 70.0 + best_kw * 25.0  # 70–95 range

            if file_id in results_map:
                existing = results_map[file_id]
                if best_kw > 0.5:
                    existing["relevance_score"] = min(100, max(
                        existing["relevance_score"],
                        text_relevance
                    ))
                    if existing["match_type"] == "visual":
                        existing["match_type"] = "visual+text"
            else:
                results_map[file_id] = {
                    "file_id":        file_id,
                    "filepath":       metadata.get("filepath", ""),
                    "filename":       filename,
                    "extension":      metadata.get("extension", ""),
                    "file_type":      metadata.get("file_type", ""),
                    "size_mb":        metadata.get("size_mb", 0),
                    "created":        metadata.get("created", ""),
                    "modified":       metadata.get("modified", ""),
                    "relevance_score": round(text_relevance, 1),
                    "date_taken":     metadata.get("date_taken", ""),
                    "camera_model":   metadata.get("camera_model", ""),
                    "ocr_text":       ocr_text,
                    "match_type":     "text",
                }
    except Exception:
        pass  # Text search failure shouldn't break visual search

    # Sort by relevance descending
    results = sorted(results_map.values(), key=lambda x: x["relevance_score"], reverse=True)

    # Apply minimum score filter
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
