"""
File metadata extraction — EXIF data, file stats, and thumbnail generation.
"""

import os
import hashlib
from datetime import datetime
from typing import Optional
from PIL import Image
import exifread


def get_file_hash(filepath: str) -> str:
    """Generate a unique hash for a file (path-based for speed, md5 for content)."""
    # Use path + mtime for fast change detection
    stat = os.stat(filepath)
    raw = f"{filepath}|{stat.st_size}|{stat.st_mtime}"
    return hashlib.md5(raw.encode()).hexdigest()


def get_file_id(filepath: str) -> str:
    """Generate a stable unique ID for a file based on its absolute path."""
    return hashlib.md5(os.path.abspath(filepath).encode()).hexdigest()


def extract_metadata(filepath: str) -> dict:
    """
    Extract metadata from a file.
    Returns a flat dict suitable for ChromaDB metadata storage.
    """
    stat = os.stat(filepath)
    _, ext = os.path.splitext(filepath)
    abspath = os.path.abspath(filepath)

    meta = {
        "filepath": abspath,
        "filename": os.path.basename(filepath),
        "folder_path": os.path.dirname(abspath),  # Add folder for filtering
        "extension": ext.lower(),
        "size_bytes": stat.st_size,
        "size_mb": round(stat.st_size / (1024 * 1024), 2),
        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "last_modified": int(stat.st_mtime),  # Unix timestamp for incremental indexing
        "file_hash": get_file_hash(filepath),
        "last_indexed": int(datetime.now().timestamp()),  # When we indexed this file
        "file_type": _classify_file_type(ext.lower()),
    }

    # Extract EXIF for images
    if meta["file_type"] == "image":
        exif = _extract_exif(filepath)
        if exif:
            meta.update(exif)

    return meta


def _classify_file_type(ext: str) -> str:
    """Classify file extension into a category."""
    from app.core.config import get_settings
    settings = get_settings()
    if ext in settings.image_extensions:
        return "image"
    elif ext in settings.document_extensions:
        return "document"
    else:
        return "other"


def _extract_exif(filepath: str) -> Optional[dict]:
    """Extract EXIF data from an image file."""
    try:
        with open(filepath, "rb") as f:
            tags = exifread.process_file(f, stop_tag="UNDEF", details=False)

        exif_data = {}

        # Date taken
        for tag_name in ["EXIF DateTimeOriginal", "EXIF DateTimeDigitized", "Image DateTime"]:
            if tag_name in tags:
                exif_data["date_taken"] = str(tags[tag_name])
                break

        # Camera info
        if "Image Make" in tags:
            exif_data["camera_make"] = str(tags["Image Make"])
        if "Image Model" in tags:
            exif_data["camera_model"] = str(tags["Image Model"])

        # Image dimensions
        if "EXIF ExifImageWidth" in tags:
            exif_data["image_width"] = str(tags["EXIF ExifImageWidth"])
        if "EXIF ExifImageLength" in tags:
            exif_data["image_height"] = str(tags["EXIF ExifImageLength"])

        # GPS (stored as strings, not floats, for ChromaDB compatibility)
        if "GPS GPSLatitude" in tags and "GPS GPSLongitude" in tags:
            exif_data["gps_latitude"] = str(tags["GPS GPSLatitude"])
            exif_data["gps_longitude"] = str(tags["GPS GPSLongitude"])

        return exif_data if exif_data else None

    except Exception:
        return None


def generate_thumbnail(
    filepath: str,
    output_dir: str,
    max_dim: int = 256,
) -> Optional[str]:
    """
    Generate a thumbnail for an image file.
    Returns the path to the saved thumbnail, or None on failure.
    """
    try:
        file_id = get_file_id(filepath)
        thumb_path = os.path.join(output_dir, f"{file_id}.webp")

        # Skip if thumbnail already exists
        if os.path.exists(thumb_path):
            return thumb_path

        with Image.open(filepath) as img:
            img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
            # Convert to RGB if needed (e.g., RGBA PNGs)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.save(thumb_path, "WEBP", quality=80)

        return thumb_path
    except Exception:
        return None
