"""
File scanner and indexing engine.
Scans directories, generates embeddings, and stores them in the vector DB.
Supports incremental indexing (skip unchanged files).
Also extracts faces (for face search) and OCR text (for text-in-image search).
"""

import os
import time
import asyncio
from typing import Optional
from dataclasses import dataclass, field
from PIL import Image

from app.core.config import get_settings
from app.core.metadata import extract_metadata, get_file_id, get_file_hash, generate_thumbnail
from app.ai.clip_embed import CLIPEmbedder
from app.db.vector_store import VectorStore, FaceStore


@dataclass
class IndexingProgress:
    """Tracks current indexing job progress."""
    total_files: int = 0
    processed: int = 0
    skipped: int = 0
    failed: int = 0
    errors: list[str] = field(default_factory=list)
    is_running: bool = False
    started_at: Optional[float] = None
    finished_at: Optional[float] = None
    current_file: str = ""
    faces_found: int = 0
    ocr_extracted: int = 0

    @property
    def elapsed_seconds(self) -> float:
        if self.started_at is None:
            return 0
        end = self.finished_at or time.time()
        return end - self.started_at

    @property
    def files_per_second(self) -> float:
        elapsed = self.elapsed_seconds
        if elapsed == 0:
            return 0
        return self.processed / elapsed

    @property
    def eta_seconds(self) -> float:
        fps = self.files_per_second
        if fps == 0:
            return 0
        remaining = self.total_files - self.processed - self.skipped
        return remaining / fps

    @property
    def percent_complete(self) -> float:
        if self.total_files == 0:
            return 0
        return ((self.processed + self.skipped) / self.total_files) * 100

    def to_dict(self) -> dict:
        return {
            "total_files": self.total_files,
            "processed": self.processed,
            "skipped": self.skipped,
            "failed": self.failed,
            "is_running": self.is_running,
            "percent_complete": round(self.percent_complete, 1),
            "files_per_second": round(self.files_per_second, 1),
            "eta_seconds": round(self.eta_seconds),
            "elapsed_seconds": round(self.elapsed_seconds),
            "current_file": self.current_file,
            "error_count": len(self.errors),
            "faces_found": self.faces_found,
            "ocr_extracted": self.ocr_extracted,
        }


# Global progress tracker (single indexing job at a time)
_current_progress = IndexingProgress()


def get_progress() -> IndexingProgress:
    return _current_progress


def compare_files_for_incremental(
    current_files: list[str],
    indexed_files: dict,
) -> tuple[list[str], list[str], list[str]]:
    """
    Compare current filesystem state with indexed files.
    Returns (new_files, modified_files, deleted_files).
    
    Args:
        current_files: List of file paths found in filesystem
        indexed_files: Dict of {filepath: metadata} from database
    """
    new_files = []
    modified_files = []
    deleted_files = []
    
    # Convert current files to set for faster lookup
    current_set = set(current_files)
    indexed_set = set(indexed_files.keys())
    
    # Find new files (in filesystem, not in database)
    new_files = list(current_set - indexed_set)
    
    # Find potentially modified files (in both, but check if changed)
    common_files = current_set & indexed_set
    for filepath in common_files:
        try:
            # Check if file has been modified since last index
            current_mtime = int(os.stat(filepath).st_mtime)
            indexed_mtime = indexed_files[filepath].get("last_modified", 0)
            
            if current_mtime > indexed_mtime:
                modified_files.append(filepath)
        except (OSError, FileNotFoundError):
            # File might have been deleted between scan and check
            deleted_files.append(filepath)
    
    # Find deleted files (in database, not in filesystem)
    deleted_files.extend(list(indexed_set - current_set))
    
    return new_files, modified_files, deleted_files


def scan_directory(root_path: str) -> list[str]:
    """
    Recursively scan a directory and return all supported file paths.
    Explicitly skips videos. Only includes images and documents.
    """
    settings = get_settings()
    supported_exts = set(settings.image_extensions + settings.document_extensions)
    video_exts = set(settings.video_extensions)  # Explicitly excluded
    excluded = set(settings.excluded_folders)
    max_size = settings.max_file_size_mb * 1024 * 1024

    files = []
    skipped_videos = 0
    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if d not in excluded and not d.startswith(".")]

        for fname in filenames:
            ext = os.path.splitext(fname)[1].lower()

            # Skip videos explicitly
            if ext in video_exts:
                skipped_videos += 1
                continue

            if ext not in supported_exts:
                continue

            filepath = os.path.join(dirpath, fname)
            try:
                size = os.path.getsize(filepath)
                if size > max_size or size == 0:
                    continue
            except OSError:
                continue

            files.append(filepath)

    print(f"[Scanner] Found {len(files)} supported files in {root_path}")
    if skipped_videos > 0:
        print(f"[Scanner] Skipped {skipped_videos} video files")

    return sorted(files)


async def index_directory(
    root_path: str,
    clip_embedder: CLIPEmbedder,
    vector_store: VectorStore,
    face_embedder=None,
    face_store: Optional[FaceStore] = None,
    ocr_engine=None,
) -> IndexingProgress:
    """
    Index all supported files in a directory tree.
    Generates CLIP embeddings, extracts faces, runs OCR (if available).
    """
    global _current_progress

    settings = get_settings()

    _current_progress = IndexingProgress()
    _current_progress.is_running = True
    _current_progress.started_at = time.time()

    files = scan_directory(root_path)
    _current_progress.total_files = len(files)

    if not files:
        _current_progress.is_running = False
        _current_progress.finished_at = time.time()
        return _current_progress

    batch_size = settings.batch_size

    for i in range(0, len(files), batch_size):
        if not _current_progress.is_running:
            break

        batch = files[i : i + batch_size]
        await asyncio.to_thread(
            _process_batch_sync,
            batch, clip_embedder, vector_store, settings,
            face_embedder, face_store, ocr_engine,
        )
        await asyncio.sleep(0)

    _current_progress.is_running = False
    _current_progress.finished_at = time.time()

    print(f"[Indexer] Done! Processed: {_current_progress.processed}, "
          f"Skipped: {_current_progress.skipped}, "
          f"Failed: {_current_progress.failed}, "
          f"Faces: {_current_progress.faces_found}, "
          f"OCR: {_current_progress.ocr_extracted}, "
          f"Time: {_current_progress.elapsed_seconds:.1f}s")

    return _current_progress


async def index_directory_incremental(
    root_path: str,
    clip_embedder: CLIPEmbedder,
    vector_store: VectorStore,
    face_embedder=None,
    face_store: Optional[FaceStore] = None,
    ocr_engine=None,
) -> IndexingProgress:
    """
    Incremental indexing - only processes new, modified, or deleted files.
    Much faster than full re-indexing for large photo libraries.
    
    Returns IndexingProgress with stats about what changed.
    """
    global _current_progress
    
    settings = get_settings()
    
    _current_progress = IndexingProgress()
    _current_progress.is_running = True
    _current_progress.started_at = time.time()
    
    # Step 1: Scan filesystem
    print(f"[Incremental] Scanning filesystem: {root_path}")
    current_files = scan_directory(root_path)
    
    # Step 2: Get already indexed files from database
    print(f"[Incremental] Getting indexed files from database...")
    indexed_files = vector_store.get_all_indexed_files()
    
    # Step 3: Compare and identify changes
    print(f"[Incremental] Comparing files...")
    new_files, modified_files, deleted_files = compare_files_for_incremental(
        current_files, indexed_files
    )
    
    # Calculate total work
    files_to_process = new_files + modified_files
    _current_progress.total_files = len(files_to_process)
    
    print(f"[Incremental] Changes detected:")
    print(f"  New files: {len(new_files)}")
    print(f"  Modified files: {len(modified_files)}")
    print(f"  Deleted files: {len(deleted_files)}")
    print(f"  Total to process: {len(files_to_process)}")
    
    # Step 4: Remove deleted files from index
    if deleted_files:
        print(f"[Incremental] Removing {len(deleted_files)} deleted files...")
        removed_count = vector_store.remove_files_by_path(deleted_files)
        print(f"[Incremental] Removed {removed_count} files from index")
    
    # Step 5: Process new and modified files
    if not files_to_process:
        print("[Incremental] No files to process - index is up to date!")
        _current_progress.is_running = False
        _current_progress.finished_at = time.time()
        return _current_progress
    
    batch_size = settings.batch_size
    
    for i in range(0, len(files_to_process), batch_size):
        if not _current_progress.is_running:
            break
        
        batch = files_to_process[i : i + batch_size]
        await asyncio.to_thread(
            _process_batch_sync,
            batch, clip_embedder, vector_store, settings,
            face_embedder, face_store, ocr_engine,
        )
        await asyncio.sleep(0)
    
    _current_progress.is_running = False
    _current_progress.finished_at = time.time()
    
    print(f"[Incremental] Done! Processed: {_current_progress.processed}, "
          f"Skipped: {_current_progress.skipped}, "
          f"Failed: {_current_progress.failed}, "
          f"Time: {_current_progress.elapsed_seconds:.1f}s")
    
    return _current_progress


def _process_batch_sync(
    filepaths: list[str],
    clip_embedder: CLIPEmbedder,
    vector_store: VectorStore,
    settings,
    face_embedder=None,
    face_store: Optional[FaceStore] = None,
    ocr_engine=None,
):
    """Process a batch: extract metadata, CLIP embeddings, faces, OCR, store."""
    global _current_progress

    images_to_embed = []
    file_data = []  # (file_id, metadata, filepath)

    for filepath in filepaths:
        _current_progress.current_file = filepath
        file_id = get_file_id(filepath)

        try:
            # --- Incremental check: skip files that haven't changed ---
            existing = vector_store.get_file(file_id)
            if existing:
                current_hash = get_file_hash(filepath)
                if existing.get("file_hash") == current_hash:
                    _current_progress.skipped += 1
                    continue
                # File changed — will re-index it

            metadata = extract_metadata(filepath)

            if metadata["file_type"] == "image":
                try:
                    img = Image.open(filepath).convert("RGB")
                    images_to_embed.append(img)
                    file_data.append((file_id, metadata, filepath))
                    generate_thumbnail(filepath, settings.thumbnails_dir, settings.thumbnail_max_dim)
                except Exception:
                    # PIL can't open this format (e.g., RAW camera files)
                    # Still record it in the index with metadata, just skip CLIP embedding
                    _current_progress.failed += 1
                    continue

        except Exception as e:
            _current_progress.failed += 1
            _current_progress.errors.append(f"{filepath}: {str(e)}")
            continue

    # Batch embed all images with CLIP
    if images_to_embed:
        try:
            embeddings = clip_embedder.embed_images(images_to_embed)
            ids = [fd[0] for fd in file_data]
            metas = [fd[1] for fd in file_data]

            # Run OCR on each image and add text to metadata
            if ocr_engine:
                for fd in file_data:
                    fid, meta, fpath = fd
                    try:
                        ocr_text = ocr_engine.extract_text_from_path(fpath)
                        if ocr_text:
                            idx = ids.index(fid)
                            metas[idx]["ocr_text"] = ocr_text[:1000]
                            _current_progress.ocr_extracted += 1
                    except Exception:
                        pass

            vector_store.add_files_batch(ids, embeddings, metas)
            _current_progress.processed += len(ids)
        except Exception as e:
            _current_progress.failed += len(images_to_embed)
            _current_progress.errors.append(f"Batch embed error: {str(e)}")

    # Extract faces and store in face DB
    if face_embedder and face_store:
        for i, (fid, meta, fpath) in enumerate(file_data):
            if i < len(images_to_embed):
                try:
                    faces = face_embedder.detect_and_embed(images_to_embed[i])
                    for face_idx, face in enumerate(faces):
                        face_id = f"{fid}_face{face_idx}"
                        face_meta = {
                            "source_file_id": fid,
                            "filepath": fpath,
                            "filename": meta.get("filename", ""),
                            "box_x1": int(face["box"][0]),
                            "box_y1": int(face["box"][1]),
                            "box_x2": int(face["box"][2]),
                            "box_y2": int(face["box"][3]),
                            "confidence": round(face["confidence"], 3),
                        }
                        face_store.add_face(face_id, face["embedding"], face_meta)
                        _current_progress.faces_found += 1
                except Exception:
                    pass

    # Close images
    for img in images_to_embed:
        img.close()


def cancel_indexing():
    """Cancel the current indexing job."""
    global _current_progress
    _current_progress.is_running = False
