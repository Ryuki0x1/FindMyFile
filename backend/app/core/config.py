"""
Application configuration — loaded from environment variables or defaults.
"""

import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """App-wide settings. Override via environment variables or .env file."""

    # Server
    port: int = 8000

    # Data paths — override FINDMYPIC_DATA_DIR to store index anywhere (e.g., external drive)
    project_root: str = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..")
    )
    data_dir: str = ""
    chroma_dir: str = ""
    thumbnails_dir: str = ""
    config_file: str = ""

    # Indexing
    batch_size: int = 32
    max_threads: int = 4
    thumbnail_max_dim: int = 256
    max_file_size_mb: int = 100

    # Supported image extensions (ALL common formats — NO videos)
    image_extensions: list[str] = [
        # Standard formats
        ".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif",
        ".tiff", ".tif", ".ico", ".svg",
        # Modern formats
        ".heic", ".heif", ".avif", ".jxl",
        # RAW camera formats
        ".cr2", ".cr3", ".nef", ".arw", ".dng", ".orf",
        ".rw2", ".raf", ".srw", ".pef", ".raw", ".rwl",
        # Professional/legacy
        ".psd", ".psb", ".tga", ".pcx", ".ppm", ".pgm",
        ".pbm", ".exr", ".hdr",
        # Screenshots and misc
        ".jfif", ".jp2", ".j2k", ".wdp", ".dds",
    ]

    # Supported document extensions
    document_extensions: list[str] = [
        ".pdf", ".docx", ".doc", ".xlsx", ".xls",
        ".pptx", ".ppt", ".txt", ".csv", ".md",
        ".rtf", ".odt", ".ods", ".odp",
    ]

    # Video extensions — EXPLICITLY EXCLUDED (never indexed)
    video_extensions: list[str] = [
        ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv",
        ".webm", ".m4v", ".mpg", ".mpeg", ".3gp", ".3g2",
        ".ts", ".mts", ".m2ts", ".vob", ".ogv", ".divx",
        ".asf", ".rm", ".rmvb", ".f4v",
    ]

    # Default excluded folders
    excluded_folders: list[str] = [
        "$Recycle.Bin", "System Volume Information", "Windows",
        "Program Files", "Program Files (x86)", "ProgramData",
        "node_modules", ".git", "__pycache__", ".venv", "venv",
        "AppData", ".thumbnails", ".cache",
    ]

    def model_post_init(self, __context) -> None:
        """Set derived paths after init."""
        if not self.data_dir:
            self.data_dir = os.path.join(self.project_root, "data")
        if not self.chroma_dir:
            self.chroma_dir = os.path.join(self.data_dir, "chroma_db")
        if not self.thumbnails_dir:
            self.thumbnails_dir = os.path.join(self.data_dir, "thumbnails")
        if not self.config_file:
            self.config_file = os.path.join(self.data_dir, "config.json")

    class Config:
        env_prefix = "FINDMYPIC_"
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
