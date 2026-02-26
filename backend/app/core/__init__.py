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

    # Data paths (relative to project root)
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

    # Supported file extensions
    image_extensions: list[str] = [
        ".jpg", ".jpeg", ".png", ".webp", ".bmp",
        ".tiff", ".tif", ".gif", ".heic",
    ]
    document_extensions: list[str] = [
        ".pdf", ".docx", ".xlsx", ".pptx", ".txt", ".csv", ".md",
    ]

    # Default excluded folders
    excluded_folders: list[str] = [
        "$Recycle.Bin", "System Volume Information", "Windows",
        "Program Files", "Program Files (x86)", "ProgramData",
        "node_modules", ".git", "__pycache__", ".venv", "venv",
        "AppData",
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
