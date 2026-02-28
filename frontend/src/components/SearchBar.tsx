import { useState, useCallback, useRef, useEffect } from "react";
import { searchWithFilters, type SearchResponse } from "../services/api";
import SearchFilters, { type FilterState } from "./SearchFilters";
import "./SearchBar.css";

interface SearchBarProps {
    onResults: (results: SearchResponse | null) => void;
    onLoading: (loading: boolean) => void;
    totalIndexed: number;
}

export default function SearchBar({ onResults, onLoading, totalIndexed }: SearchBarProps) {
    const [query, setQuery] = useState("");
    const [isSearching, setIsSearching] = useState(false);
    const [history, setHistory] = useState<string[]>(() => {
        try {
            return JSON.parse(localStorage.getItem("FindMyFile_history") || "[]");
        } catch {
            return [];
        }
    });
    const [showDropdown, setShowDropdown] = useState(false);
    const inputRef = useRef<HTMLInputElement>(null);
    
    // Filter state
    const [filters, setFilters] = useState<FilterState>({
        fileType: "",
        folderPath: "",
        minScore: 0,
        extension: "",
    });
    const [nResults, setNResults] = useState(50);
    const [textOnly, setTextOnly] = useState(false);

    useEffect(() => {
        inputRef.current?.focus();
    }, []);

    const doSearch = useCallback(
        async (searchQuery: string) => {
            if (!searchQuery.trim()) {
                onResults(null);
                return;
            }

            setIsSearching(true);
            onLoading(true);

            try {
                // Use searchWithFilters to include all filter parameters
                const results = await searchWithFilters({
                    query: searchQuery.trim(),
                    nResults: nResults,
                    fileType: filters.fileType || undefined,
                    extension: filters.extension || undefined,
                    folderPath: filters.folderPath || undefined,
                    minScore: filters.minScore > 0 ? filters.minScore : undefined,
                    textOnly: textOnly,
                });
                onResults(results);

                // Save to history
                const updated = [
                    searchQuery.trim(),
                    ...history.filter((h) => h !== searchQuery.trim()),
                ].slice(0, 30);
                setHistory(updated);
                localStorage.setItem("FindMyFile_history", JSON.stringify(updated));
            } catch (err) {
                console.error("Search failed:", err);
                onResults(null);
            } finally {
                setIsSearching(false);
                onLoading(false);
            }
        },
        [history, onResults, onLoading, filters, nResults, textOnly]
    );

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        setQuery(value);
        setShowDropdown(value.length === 0 && history.length > 0);
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === "Enter") {
            e.preventDefault();
            setShowDropdown(false);
            doSearch(query);
        }
        if (e.key === "Escape") {
            setShowDropdown(false);
        }
    };

    const handleHistoryClick = (item: string) => {
        setQuery(item);
        setShowDropdown(false);
        doSearch(item);
    };

    const handleClear = () => {
        setQuery("");
        onResults(null);
        inputRef.current?.focus();
    };

    const handleClearHistory = () => {
        setHistory([]);
        localStorage.removeItem("FindMyFile_history");
        setShowDropdown(false);
    };

    const handleResetFilters = () => {
        setFilters({
            fileType: "",
            folderPath: "",
            minScore: 0,
            extension: "",
        });
        // Re-run search with cleared filters if there's a query
        if (query.trim()) {
            doSearch(query);
        }
    };

    return (
        <div className="search-container">
            <div className="search-wrapper">
                <div className={`search-box ${isSearching ? "searching" : ""}`}>
                    <svg className="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <circle cx="11" cy="11" r="8" />
                        <path d="M21 21l-4.35-4.35" />
                    </svg>
                    <input
                        ref={inputRef}
                        id="search-input"
                        type="text"
                        className="search-input"
                        placeholder="Describe what you're looking for..."
                        value={query}
                        onChange={handleInputChange}
                        onKeyDown={handleKeyDown}
                        onFocus={() => query.length === 0 && history.length > 0 && setShowDropdown(true)}
                        onBlur={() => setTimeout(() => setShowDropdown(false), 200)}
                    />
                    {query && (
                        <button className="search-clear" onClick={handleClear} aria-label="Clear">
                            ✕
                        </button>
                    )}
                    {isSearching && <div className="search-spinner" />}
                </div>

                {totalIndexed > 0 && (
                    <div className="search-hint-row">
                        <p className="search-hint">
                            Searching across <strong>{totalIndexed.toLocaleString()}</strong> indexed files
                        </p>
                        <div className="search-nresults">
                            <label htmlFor="n-results-select">Show up to:</label>
                            <select
                                id="n-results-select"
                                value={nResults}
                                onChange={(e) => setNResults(Number(e.target.value))}
                                className="nresults-select"
                            >
                                <option value={20}>20 results</option>
                                <option value={50}>50 results</option>
                                <option value={100}>100 results</option>
                                <option value={200}>200 results</option>
                                <option value={500}>500 results</option>
                                <option value={9999}>All results</option>
                            </select>
                            <label className="text-only-toggle" title="Skip visual AI — only search text found inside files">
                                <input
                                    type="checkbox"
                                    checked={textOnly}
                                    onChange={e => setTextOnly(e.target.checked)}
                                />
                                📝 Text only
                            </label>
                        </div>
                    </div>
                )}

                {showDropdown && history.length > 0 && (
                    <div className="suggestions-dropdown animate-in">
                        <div className="suggestions-section">
                            <div className="suggestions-header">
                                <p className="suggestions-label">Recent Searches</p>
                                <button
                                    className="clear-history-btn"
                                    onMouseDown={handleClearHistory}
                                >
                                    Clear all
                                </button>
                            </div>
                            {history.slice(0, 8).map((h, i) => (
                                <button key={`h-${i}`} className="suggestion-item" onMouseDown={() => handleHistoryClick(h)}>
                                    <span className="suggestion-icon">🕐</span> {h}
                                </button>
                            ))}
                        </div>
                    </div>
                )}
            </div>

            {/* Search Filters */}
            <SearchFilters
                filters={filters}
                onChange={setFilters}
                onReset={handleResetFilters}
                disabled={isSearching}
            />
        </div>
    );
}

