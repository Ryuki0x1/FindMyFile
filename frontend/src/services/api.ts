/**
 * FindMyPic API Client
 * Connects the React frontend to the Python FastAPI backend.
 */

const API_BASE = "http://127.0.0.1:8000/api";

// --- Types ---

export interface SearchResult {
  file_id: string;
  filepath: string;
  filename: string;
  extension: string;
  file_type: string;
  size_mb: number;
  created: string;
  modified: string;
  relevance_score: number;
  date_taken?: string;
  camera_model?: string;
  ocr_text?: string;
  match_type?: string;
  face_box?: { x1: number; y1: number; x2: number; y2: number };
  confidence?: number;
}

export interface SearchResponse {
  query: string;
  total_results: number;
  results: SearchResult[];
}

export interface IndexProgress {
  total_files: number;
  processed: number;
  skipped: number;
  failed: number;
  is_running: boolean;
  percent_complete: number;
  files_per_second: number;
  eta_seconds: number;
  elapsed_seconds: number;
  current_file: string;
  error_count: number;
  faces_found: number;
  ocr_extracted: number;
}

export interface SystemInfo {
  gpu: {
    name: string;
    vram_mb: number;
    vram_gb: number;
    cuda_available: boolean;
    driver: string;
  };
  system: {
    ram_gb: number;
    cpu_count: number;
    os: string;
    os_version: string;
  };
  recommendation: {
    tier: number;
    tier_name: string;
    description: string;
    clip_model: string;
    captioner_model: string;
    text_embed_model: string;
    total_download_mb: number;
    estimated_speed: string;
  };
}

export interface ScanResult {
  total_files: number;
  breakdown: Record<string, number>;
}

export interface AppSettings {
  indexed_folders: string[];
  total_indexed_files: number;
  excluded_folders: string[];
  image_extensions: string[];
  document_extensions: string[];
  video_extensions_excluded: string[];
  batch_size: number;
  max_file_size_mb: number;
  data_dir: string;
  chroma_dir: string;
  thumbnails_dir: string;
}

// --- API calls ---

async function apiFetch<T>(
  path: string,
  options?: RequestInit
): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const error = await res.text();
    throw new Error(`API Error ${res.status}: ${error}`);
  }
  return res.json();
}

export interface SearchFilters {
  query: string;
  nResults?: number;
  fileType?: string;
  extension?: string;
  folderPath?: string;
  minScore?: number;
}

/** Search indexed files with natural language */
export async function searchFiles(
  query: string,
  nResults = 20,
  fileType?: string,
  extension?: string,
  folderPath?: string,
  minScore?: number
): Promise<SearchResponse> {
  return apiFetch<SearchResponse>("/search/", {
    method: "POST",
    body: JSON.stringify({
      query,
      n_results: nResults,
      file_type: fileType || null,
      extension: extension || null,
      folder_path: folderPath || null,
      min_score: minScore || null,
    }),
  });
}

/** Search with full filter object */
export async function searchWithFilters(filters: SearchFilters): Promise<SearchResponse> {
  return searchFiles(
    filters.query,
    filters.nResults,
    filters.fileType,
    filters.extension,
    filters.folderPath,
    filters.minScore
  );
}

/** Start indexing files in the given paths */
export async function startIndexing(paths: string[]): Promise<{ status: string; message: string }> {
  return apiFetch("/index/start", {
    method: "POST",
    body: JSON.stringify({ paths }),
  });
}

/** Get current indexing progress */
export async function getIndexProgress(): Promise<IndexProgress> {
  return apiFetch<IndexProgress>("/index/progress");
}

/** Cancel current indexing job */
export async function cancelIndexing(): Promise<{ status: string }> {
  return apiFetch("/index/cancel", { method: "POST" });
}

/** Dry-run scan to count files before indexing */
export async function scanFiles(paths: string[]): Promise<ScanResult> {
  return apiFetch<ScanResult>("/index/scan", {
    method: "POST",
    body: JSON.stringify({ paths }),
  });
}

/** Get system info (GPU, RAM, tier recommendation) */
export async function getSystemInfo(): Promise<SystemInfo> {
  return apiFetch<SystemInfo>("/settings/system-info");
}

/** Get current app settings */
export async function getSettings(): Promise<AppSettings> {
  return apiFetch<AppSettings>("/settings/");
}

/** Clear all indexed data */
export async function clearIndex(): Promise<{ status: string }> {
  return apiFetch("/settings/clear-index", { method: "POST" });
}

/** Get search index stats */
export async function getSearchStats(): Promise<{ total_files: number; persist_dir: string }> {
  return apiFetch("/search/stats");
}

/** Get thumbnail URL for a file */
export function getThumbnailUrl(fileId: string): string {
  return `http://127.0.0.1:8000/thumbnails/${fileId}.webp`;
}

/** Get URL to view a local file via the backend proxy */
export function getFileUrl(filepath: string): string {
  return `http://127.0.0.1:8000/api/file?path=${encodeURIComponent(filepath)}`;
}

/** Search for photos with a matching face */
export async function faceSearch(file: File, nResults = 50): Promise<SearchResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/search/face?n_results=${nResults}`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(error.detail || `Face search failed: ${res.status}`);
  }
  return res.json();
}

/** Check if backend is reachable */
export async function healthCheck(): Promise<boolean> {
  try {
    const res = await fetch("http://127.0.0.1:8000/", { signal: AbortSignal.timeout(10000) });
    return res.ok;
  } catch {
    return false;
  }
}
