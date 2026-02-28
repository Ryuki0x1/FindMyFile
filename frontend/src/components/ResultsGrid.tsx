import { useState } from "react";
import type { SearchResult } from "../services/api";
import { getThumbnailUrl, getFileUrl } from "../services/api";
import "./ResultsGrid.css";

/** Highlights all occurrences of query words inside text */
function HighlightedText({ text, query }: { text: string; query: string }) {
    if (!query || !text) return <>{text}</>;
    // Build a regex from all non-trivial words in the query
    const words = query
        .split(/\W+/)
        .filter(w => w.length >= 2)
        .map(w => w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
    if (words.length === 0) return <>{text}</>;
    const pattern = new RegExp(`(${words.join("|")})`, "gi");
    const parts = text.split(pattern);
    return (
        <>
            {parts.map((part, i) =>
                pattern.test(part)
                    ? <mark key={i} className="ocr-highlight">{part}</mark>
                    : <span key={i}>{part}</span>
            )}
        </>
    );
}

const PAGE_SIZE = 50;

interface ResultsGridProps {
    results: SearchResult[];
    query: string;
    onFileClick: (result: SearchResult) => void;
}

export default function ResultsGrid({ results, query, onFileClick }: ResultsGridProps) {
    const [viewMode, setViewMode] = useState<"grid" | "list">("grid");
    const [page, setPage] = useState(1);

    const totalPages = Math.max(1, Math.ceil(results.length / PAGE_SIZE));
    const safePage = Math.min(page, totalPages);
    const pageStart = (safePage - 1) * PAGE_SIZE;
    const pageEnd = pageStart + PAGE_SIZE;
    const pageResults = results.slice(pageStart, pageEnd);

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
                    {totalPages > 1 && (
                        <span className="results-page-info">
                            — page {safePage} of {totalPages}
                        </span>
                    )}
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
                {pageResults.map((result, index) => (
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
                                    📝 <HighlightedText text={result.ocr_text.slice(0, 120)} query={query} />
                                    {result.ocr_text.length > 120 ? "…" : ""}
                                </p>
                            )}
                        </div>
                    </div>
                ))}
            </div>
            {/* Pagination */}
            {totalPages > 1 && (
                <div className="results-pagination">
                    <button
                        className="btn btn-ghost pag-btn"
                        onClick={() => setPage(1)}
                        disabled={safePage === 1}
                    >«</button>
                    <button
                        className="btn btn-ghost pag-btn"
                        onClick={() => setPage(p => Math.max(1, p - 1))}
                        disabled={safePage === 1}
                    >‹ Prev</button>

                    {Array.from({ length: totalPages }, (_, i) => i + 1)
                        .filter(p => p === 1 || p === totalPages || Math.abs(p - safePage) <= 2)
                        .reduce<(number | "...")[]>((acc, p, idx, arr) => {
                            if (idx > 0 && p - (arr[idx - 1] as number) > 1) acc.push("...");
                            acc.push(p);
                            return acc;
                        }, [])
                        .map((p, i) =>
                            p === "..." ? (
                                <span key={`e-${i}`} className="pag-ellipsis">…</span>
                            ) : (
                                <button
                                    key={p}
                                    className={`btn pag-btn ${safePage === p ? "pag-active" : "btn-ghost"}`}
                                    onClick={() => setPage(p as number)}
                                >{p}</button>
                            )
                        )
                    }

                    <button
                        className="btn btn-ghost pag-btn"
                        onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                        disabled={safePage === totalPages}
                    >Next ›</button>
                    <button
                        className="btn btn-ghost pag-btn"
                        onClick={() => setPage(totalPages)}
                        disabled={safePage === totalPages}
                    >»</button>

                    <span className="pag-info">
                        {pageStart + 1}–{Math.min(pageEnd, results.length)} of {results.length}
                    </span>
                </div>
            )}
        </div>
    );
}
