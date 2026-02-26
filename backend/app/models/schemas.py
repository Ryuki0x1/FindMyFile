"""
Pydantic models for API request/response schemas.
"""

from pydantic import BaseModel, Field
from typing import Optional


# --- Search ---

class SearchRequest(BaseModel):
    query: str = Field(..., description="Natural language search query", min_length=1)
    n_results: int = Field(20, description="Max results to return", ge=1, le=100)
    file_type: Optional[str] = Field(None, description="Filter: 'image' or 'document'")
    extension: Optional[str] = Field(None, description="Filter: e.g. '.jpg', '.pdf'")
    folder_path: Optional[str] = Field(None, description="Filter: search only in specific folder")
    min_score: Optional[float] = Field(None, description="Minimum relevance score (0-100)", ge=0, le=100)


class SearchResult(BaseModel):
    file_id: str
    filepath: str
    filename: str
    extension: str = ""
    file_type: str = ""
    size_mb: float = 0
    created: str = ""
    modified: str = ""
    relevance_score: float
    date_taken: Optional[str] = None
    camera_model: Optional[str] = None
    ocr_text: Optional[str] = None
    match_type: Optional[str] = None


class SearchResponse(BaseModel):
    query: str
    total_results: int
    results: list[SearchResult]
    filters_applied: Optional[dict] = None


# --- Indexing ---

class IndexRequest(BaseModel):
    paths: list[str] = Field(..., description="List of folder/drive paths to index")


class IndexProgressResponse(BaseModel):
    total_files: int
    processed: int
    skipped: int
    failed: int
    is_running: bool
    percent_complete: float
    files_per_second: float
    eta_seconds: float
    elapsed_seconds: float
    current_file: str
    error_count: int
    faces_found: int = 0
    ocr_extracted: int = 0


# --- Settings ---

class SettingsResponse(BaseModel):
    indexed_folders: list[str]
    total_indexed_files: int
    excluded_folders: list[str]
    image_extensions: list[str]
    document_extensions: list[str]
    batch_size: int
    max_file_size_mb: int


class UpdateSettingsRequest(BaseModel):
    excluded_folders: Optional[list[str]] = None
    batch_size: Optional[int] = None
    max_file_size_mb: Optional[int] = None


# --- System / GPU ---

class GPUInfoResponse(BaseModel):
    gpu_name: str
    vram_gb: float
    cuda_available: bool
    ram_gb: float
    recommended_tier: int
    tier_name: str
    description: str
    total_download_mb: int
    estimated_speed: str
