import { useState } from "react";
import type { SearchResult } from "../services/api";
import { getThumbnailUrl, getFileUrl } from "../services/api";
import "./ResultsGrid.css";

interface ResultsGridProps {
    results: SearchResult[];
    query: string;
    onFileClick: (result: SearchResult) => void;
}

export default function ResultsGrid({ results, query, onFileClick }: ResultsGridProps) {
    const [viewMode, setViewMode] = useState<"grid" | "list">("grid");

    if (results.length === 0) {
        return (
            <div className="no-results animate-in">
                <div className="no-results-icon">🔍</div>
                <h3>No results found</h3>
                <p>Try a different description or check if the folder is indexed.</p>
            </div>
        );
    }

    return (
        <div className="results-container animate-in">
            <div className="results-header">
                <div className="results-info">
                    <span className="results-count">{results.length} results</span>
                    <span className="results-query">for "{query}"</span>
                </div>
                <div className="results-controls">
                    <button
                        className={`btn btn-icon ${viewMode === "grid" ? "active" : ""}`}
                        onClick={() => setViewMode("grid")}
                        aria-label="Grid view"
                    >
                        <svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16">
                            <rect x="3" y="3" width="7" height="7" rx="1.5" />
                            <rect x="14" y="3" width="7" height="7" rx="1.5" />
                            <rect x="3" y="14" width="7" height="7" rx="1.5" />
                            <rect x="14" y="14" width="7" height="7" rx="1.5" />
                        </svg>
                    </button>
                    <button
                        className={`btn btn-icon ${viewMode === "list" ? "active" : ""}`}
                        onClick={() => setViewMode("list")}
                        aria-label="List view"
                    >
                        <svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16">
                            <rect x="3" y="4" width="18" height="3" rx="1" />
                            <rect x="3" y="10.5" width="18" height="3" rx="1" />
                            <rect x="3" y="17" width="18" height="3" rx="1" />
                        </svg>
                    </button>
                </div>
            </div>

            <div className={`results-${viewMode}`}>
                {results.map((result, index) => (
                    <div
                        key={result.file_id}
                        className={`result-card result-card-${viewMode}`}
                        onClick={() => onFileClick(result)}
                        style={{ animationDelay: `${index * 0.04}s` }}
                    >
                        <div className="result-thumbnail">
                            {result.file_type === "image" ? (
                                <img
                                    src={getThumbnailUrl(result.file_id)}
                                    alt={result.filename}
                                    loading="lazy"
                                    onError={(e) => {
                                        const img = e.target as HTMLImageElement;
                                        // Fallback: try full image via backend proxy
                                        if (!img.dataset.fallback) {
                                            img.dataset.fallback = "1";
                                            img.src = getFileUrl(result.filepath);
                                        } else {
                                            img.style.display = "none";
                                            img.nextElementSibling?.classList.remove("hidden");
                                        }
                                    }}
                                />
                            ) : null}
                            <div className={`result-placeholder ${result.file_type === "image" ? "hidden" : ""}`}>
                                <span className="result-ext">{result.extension}</span>
                            </div>
                        </div>

                        <div className="result-info">
                            <p className="result-filename" title={result.filename}>
                                {result.filename}
                            </p>
                            <p className="result-path" title={result.filepath}>
                                {result.filepath}
                            </p>
                            <div className="result-meta">
                                <span className="badge badge-accent">{result.relevance_score}%</span>
                                {result.match_type === "text" && <span className="badge badge-text" title="Found via text in image">📝 Text Match</span>}
                                {result.match_type === "visual+text" && <span className="badge badge-text" title="Matched visually + text in image">🔍📝 Visual+Text</span>}
                                {result.match_type === "face" && <span className="badge badge-face" title="Face match">👤 Face</span>}
                                {result.size_mb > 0 && <span className="result-size">{result.size_mb} MB</span>}
                                {result.date_taken && <span className="result-date">{result.date_taken}</span>}
                            </div>
                            {result.ocr_text && (
                                <p className="result-ocr" title={result.ocr_text}>
                                    📝 {result.ocr_text.slice(0, 80)}{result.ocr_text.length > 80 ? "..." : ""}
                                </p>
                            )}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
