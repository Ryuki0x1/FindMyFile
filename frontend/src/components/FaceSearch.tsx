import { useState, useRef } from "react";
import { faceSearch, type SearchResponse } from "../services/api";
import "./FaceSearch.css";

interface FaceSearchProps {
    onResults: (results: SearchResponse | null) => void;
}

export default function FaceSearch({ onResults }: FaceSearchProps) {
    const [isSearching, setIsSearching] = useState(false);
    const [preview, setPreview] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;

        setError(null);

        // Show preview of the selected face
        const reader = new FileReader();
        reader.onload = () => setPreview(reader.result as string);
        reader.readAsDataURL(file);

        // Perform face search
        setIsSearching(true);
        try {
            const results = await faceSearch(file);
            onResults(results);
        } catch (err: any) {
            setError(err.message || "Face search failed");
            onResults(null);
        } finally {
            setIsSearching(false);
        }
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
                                <span>Searching faces...</span>
                            </div>
                        )}
                    </div>
                    <button className="face-clear-btn" onClick={handleClear}>
                        ✕ Clear
                    </button>
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
