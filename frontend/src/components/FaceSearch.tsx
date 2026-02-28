import { useState, useRef, useEffect } from "react";
import { faceSearch, getIndexedFolders, type SearchResponse } from "../services/api";
import "./FaceSearch.css";

interface FaceSearchProps {
    onResults: (results: SearchResponse | null) => void;
}

export default function FaceSearch({ onResults }: FaceSearchProps) {
    const [isSearching, setIsSearching] = useState(false);
    const [preview, setPreview] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [threshold, setThreshold] = useState(50);
    const [lastFile, setLastFile] = useState<File | null>(null);
    const [folderScope, setFolderScope] = useState("");
    const [indexedFolders, setIndexedFolders] = useState<string[]>([]);
    const fileInputRef = useRef<HTMLInputElement>(null);

    // Load indexed folders on mount
    useEffect(() => {
        getIndexedFolders()
            .then(res => setIndexedFolders(res.folders))
            .catch(() => setIndexedFolders([]));
    }, []);

    const runSearch = async (file: File, thresh: number, folder: string) => {
        setIsSearching(true);
        setError(null);
        try {
            const results = await faceSearch(file, 50, thresh / 100, folder || undefined);
            onResults(results);
        } catch (err: any) {
            setError(err.message || "Face search failed");
            onResults(null);
        } finally {
            setIsSearching(false);
        }
    };

    const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;
        setLastFile(file);
        setError(null);

        const reader = new FileReader();
        reader.onload = () => setPreview(reader.result as string);
        reader.readAsDataURL(file);

        await runSearch(file, threshold, folderScope);
    };

    const handleThresholdChange = async (val: number) => {
        setThreshold(val);
        if (lastFile) await runSearch(lastFile, val, folderScope);
    };

    const handleFolderChange = async (val: string) => {
        setFolderScope(val);
        if (lastFile) await runSearch(lastFile, threshold, val);
    };

    const handleClick = () => {
        fileInputRef.current?.click();
    };

    const handleClear = () => {
        setPreview(null);
        setError(null);
        onResults(null);
        if (fileInputRef.current) {
            fileInputRef.current.value = "";
        }
    };

    return (
        <div className="face-search">
            <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleFileSelect}
                style={{ display: "none" }}
                id="face-upload-input"
            />

            {!preview ? (
                <button
                    className="face-search-btn"
                    onClick={handleClick}
                    disabled={isSearching}
                    id="face-search-trigger"
                >
                    <span className="face-search-icon">👤</span>
                    <span className="face-search-label">Find by Face</span>
                    <span className="face-search-hint">Upload a photo to find all matching faces</span>
                </button>
            ) : (
                <div className="face-search-active">
                    <div className="face-preview-wrapper">
                        <img src={preview} alt="Reference face" className="face-preview-img" />
                        {isSearching && (
                            <div className="face-search-overlay">
                                <div className="face-spinner" />
                                <span>Searching...</span>
                            </div>
                        )}
                    </div>
                    <div className="face-controls">

                        {/* Strictness slider */}
                        <div className="face-threshold">
                            <div className="face-control-header">
                                <span className="face-control-label">Match strictness</span>
                                <span className="face-control-value">{threshold}%</span>
                            </div>
                            <input
                                type="range"
                                min={20}
                                max={90}
                                step={5}
                                value={threshold}
                                onChange={e => handleThresholdChange(Number(e.target.value))}
                                className="face-threshold-slider"
                                disabled={isSearching}
                            />
                            <div className="face-threshold-labels">
                                <span>Loose</span>
                                <span>Balanced</span>
                                <span>Strict</span>
                            </div>
                            <p className="face-threshold-hint">
                                {threshold >= 75 ? "⚡ Strict — exact matches only" :
                                 threshold >= 50 ? "✅ Balanced — same person, different lighting" :
                                 "🔍 Loose — may include similar-looking people"}
                            </p>
                        </div>

                        {/* Folder scope */}
                        {indexedFolders.length > 0 && (
                            <div className="face-scope-row">
                                <div className="face-control-header">
                                    <span className="face-control-label">📁 Search in</span>
                                    {folderScope && (
                                        <button
                                            className="face-scope-clear"
                                            onClick={() => handleFolderChange("")}
                                            disabled={isSearching}
                                        >✕ All</button>
                                    )}
                                </div>
                                <select
                                    className="face-scope-select"
                                    value={folderScope}
                                    onChange={e => handleFolderChange(e.target.value)}
                                    disabled={isSearching}
                                >
                                    <option value="">All indexed folders</option>
                                    {indexedFolders.map(f => (
                                        <option key={f} value={f}>{f}</option>
                                    ))}
                                </select>
                            </div>
                        )}

                        {/* Actions */}
                        <div className="face-actions">
                            <button className="btn btn-ghost face-change-btn" onClick={handleClick} disabled={isSearching}>
                                🔄 Change Photo
                            </button>
                            <button className="btn btn-danger face-clear-btn" onClick={handleClear}>
                                ✕ Clear
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {error && (
                <div className="face-search-error">
                    <span>⚠️</span> {error}
                </div>
            )}
        </div>
    );
}
