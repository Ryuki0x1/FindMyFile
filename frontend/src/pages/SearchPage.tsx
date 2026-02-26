import { useState, useCallback } from "react";
import SearchBar from "../components/SearchBar";
import FaceSearch from "../components/FaceSearch";
import ResultsGrid from "../components/ResultsGrid";
import FilePreview from "../components/FilePreview";
import { type SearchResponse, type SearchResult } from "../services/api";
import "./SearchPage.css";

type SearchMode = "text" | "face";

interface SearchPageProps {
    totalIndexed: number;
}

export default function SearchPage({ totalIndexed }: SearchPageProps) {
    const [searchResults, setSearchResults] = useState<SearchResponse | null>(null);
    const [selectedFile, setSelectedFile] = useState<SearchResult | null>(null);
    const [searchMode, setSearchMode] = useState<SearchMode>("text");

    const handleResults = useCallback((results: SearchResponse | null) => {
        setSearchResults(results);
    }, []);

    const handleLoading = useCallback((_loading: boolean) => {
        // Loading state handled by SearchBar internally
    }, []);

    const switchMode = (mode: SearchMode) => {
        setSearchMode(mode);
        setSearchResults(null);
    };

    return (
        <div className="search-page">
            {/* Hero Section (shown when no search results) */}
            {!searchResults && (
                <div className="hero-section animate-in">
                    <h2 className="hero-title">
                        Search your files with <span className="gradient-text">AI</span>
                    </h2>
                    <p className="hero-subtitle">
                        Describe what you're looking for, search text inside images, or find someone by face.
                    </p>
                </div>
            )}

            {/* Search Mode Toggle */}
            <div className="search-mode-toggle">
                <button
                    className={`mode-btn ${searchMode === "text" ? "active" : ""}`}
                    onClick={() => switchMode("text")}
                    id="mode-text-search"
                >
                    <span className="mode-icon">🔍</span>
                    <span>Text / Visual Search</span>
                </button>
                <button
                    className={`mode-btn ${searchMode === "face" ? "active" : ""}`}
                    onClick={() => switchMode("face")}
                    id="mode-face-search"
                >
                    <span className="mode-icon">👤</span>
                    <span>Face Search</span>
                </button>
            </div>

            {/* Search Input */}
            {searchMode === "text" ? (
                <SearchBar
                    onResults={handleResults}
                    onLoading={handleLoading}
                    totalIndexed={totalIndexed}
                />
            ) : (
                <FaceSearch onResults={handleResults} />
            )}

            {/* Results */}
            {searchResults && (
                <ResultsGrid
                    results={searchResults.results}
                    query={searchResults.query}
                    onFileClick={setSelectedFile}
                />
            )}

            {/* File Preview Modal */}
            {selectedFile && (
                <FilePreview file={selectedFile} onClose={() => setSelectedFile(null)} />
            )}
        </div>
    );
}
