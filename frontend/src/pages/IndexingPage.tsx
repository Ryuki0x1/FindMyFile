import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import {
    getIndexProgress,
    cancelIndexing,
    startIndexing,
    scanFiles,
    type IndexProgress,
} from "../services/api";
import "./IndexingPage.css";
import "./SettingsPage.css";

export default function IndexingPage() {
    const navigate = useNavigate();
    const [progress, setProgress] = useState<IndexProgress | null>(null);
    const [folders, setFolders] = useState<string[]>(() => {
        try {
            return JSON.parse(localStorage.getItem("FindMyFile_indexed_folders") || "[]");
        } catch {
            return [];
        }
    });
    const [newFolder, setNewFolder] = useState("");
    const [error, setError] = useState("");
    const [isStarting, setIsStarting] = useState(false);
    const [isScanning, setIsScanning] = useState(false);
    const [scanResult, setScanResult] = useState<number | null>(null);
    const intervalRef = useRef<ReturnType<typeof setInterval>>(undefined);

    useEffect(() => {
        const poll = async () => {
            try {
                const p = await getIndexProgress();
                setProgress(p);
            } catch { /* backend not reachable */ }
        };
        poll();
        intervalRef.current = setInterval(poll, 1000);
        return () => clearInterval(intervalRef.current);
    }, []);

    const formatTime = (seconds: number) => {
        if (seconds < 60) return `${Math.round(seconds)}s`;
        if (seconds < 3600) return `${Math.floor(seconds / 60)}m ${Math.round(seconds % 60)}s`;
        return `${Math.floor(seconds / 3600)}h ${Math.floor((seconds % 3600) / 60)}m`;
    };

    const handleAddFolder = () => {
        const path = newFolder.trim();
        if (path && !folders.includes(path)) {
            const updated = [...folders, path];
            setFolders(updated);
            localStorage.setItem("FindMyFile_indexed_folders", JSON.stringify(updated));
            setNewFolder("");
            setError("");
            setScanResult(null);
        }
    };

    const handleRemoveFolder = (path: string) => {
        const updated = folders.filter((f) => f !== path);
        setFolders(updated);
        localStorage.setItem("FindMyFile_indexed_folders", JSON.stringify(updated));
        setScanResult(null);
    };

    const handleScan = async () => {
        if (folders.length === 0) return;
        setIsScanning(true);
        setError("");
        try {
            const result = await scanFiles(folders);
            setScanResult(result.total_files);
        } catch (err: any) {
            setError(err.message || "Failed to scan folders.");
        }
        setIsScanning(false);
    };

    const handleStartIndexing = async () => {
        if (folders.length === 0) return;
        setIsStarting(true);
        setError("");
        try {
            await startIndexing(folders);
            localStorage.setItem("FindMyFile_setup_done", "true");
            localStorage.setItem("FindMyFile_indexed_folders", JSON.stringify(folders));
        } catch (err: any) {
            setError(err.message || "Failed to start indexing.");
        }
        setIsStarting(false);
    };

    const handleCancel = async () => {
        try {
            await cancelIndexing();
        } catch { /* ignore */ }
    };

    const isRunning = progress?.is_running ?? false;
    const hasFinished = !isRunning && (progress?.total_files ?? 0) > 0 && (progress?.processed ?? 0) > 0;

    return (
        <div className="indexing-page animate-in">
            <div className="page-header">
                <button className="btn btn-ghost back-btn" onClick={() => navigate(-1)}>
                    ← Back
                </button>
                <h1 className="page-title">
                    <span className="page-icon">📊</span> Indexing
                </h1>
            </div>

            {error && <div className="settings-alert alert-error">{error}</div>}

            {/* Live Progress Section */}
            {(isRunning || hasFinished) && progress && (
                <section className="idx-section idx-progress-section">
                    <div className="idx-status-row">
                        <div className="idx-status-badge">
                            {isRunning ? (
                                <>
                                    <div className="status-dot status-active" />
                                    <span>Indexing in progress…</span>
                                </>
                            ) : (
                                <>
                                    <div className="status-dot status-done" />
                                    <span>Indexing complete</span>
                                </>
                            )}
                        </div>
                        {isRunning && (
                            <button className="btn btn-danger btn-sm" onClick={handleCancel}>
                                ✕ Cancel
                            </button>
                        )}
                    </div>

                    <div className="progress-bar idx-bar">
                        <div
                            className="progress-bar-fill"
                            style={{ width: `${progress.percent_complete}%` }}
                        />
                    </div>
                    <div className="idx-percent">{progress.percent_complete.toFixed(1)}%</div>

                    <div className="idx-stats-grid">
                        <div className="idx-stat">
                            <span className="idx-stat-val">{progress.processed.toLocaleString()}</span>
                            <span className="idx-stat-lbl">Processed</span>
                        </div>
                        <div className="idx-stat">
                            <span className="idx-stat-val">{progress.skipped.toLocaleString()}</span>
                            <span className="idx-stat-lbl">Skipped</span>
                        </div>
                        <div className="idx-stat">
                            <span className="idx-stat-val">{progress.failed.toLocaleString()}</span>
                            <span className="idx-stat-lbl">Failed</span>
                        </div>
                        <div className="idx-stat">
                            <span className="idx-stat-val">{progress.total_files.toLocaleString()}</span>
                            <span className="idx-stat-lbl">Total</span>
                        </div>
                        <div className="idx-stat">
                            <span className="idx-stat-val">{progress.faces_found.toLocaleString()}</span>
                            <span className="idx-stat-lbl">👤 Faces</span>
                        </div>
                        <div className="idx-stat">
                            <span className="idx-stat-val">{progress.ocr_extracted.toLocaleString()}</span>
                            <span className="idx-stat-lbl">📝 OCR</span>
                        </div>
                        {isRunning && (
                            <>
                                <div className="idx-stat">
                                    <span className="idx-stat-val">{progress.files_per_second}</span>
                                    <span className="idx-stat-lbl">Files/sec</span>
                                </div>
                                <div className="idx-stat">
                                    <span className="idx-stat-val">{formatTime(progress.eta_seconds)}</span>
                                    <span className="idx-stat-lbl">ETA</span>
                                </div>
                            </>
                        )}
                        {hasFinished && (
                            <div className="idx-stat">
                                <span className="idx-stat-val">{formatTime(progress.elapsed_seconds)}</span>
                                <span className="idx-stat-lbl">Time Taken</span>
                            </div>
                        )}
                    </div>

                    {isRunning && progress.current_file && (
                        <div className="idx-current-file" title={progress.current_file}>
                            <span className="current-label">Current:</span>
                            <span className="current-path">{progress.current_file}</span>
                        </div>
                    )}

                    {progress.error_count > 0 && (
                        <div className="idx-errors">
                            ⚠️ {progress.error_count} error(s) during indexing
                        </div>
                    )}
                </section>
            )}

            {/* Add Folders & Start Indexing */}
            <section className="idx-section">
                <h2 className="section-title">📂 Folders to Index</h2>
                <p className="section-desc">
                    Add folders containing your photos and documents. Videos are automatically skipped.
                    Already-indexed files are skipped too — only new/changed files get processed.
                </p>

                <div className="folder-input-row">
                    <input
                        type="text"
                        className="input"
                        placeholder="Enter folder path (e.g., E:\Photos)"
                        value={newFolder}
                        onChange={(e) => setNewFolder(e.target.value)}
                        onKeyDown={(e) => e.key === "Enter" && handleAddFolder()}
                        disabled={isRunning}
                    />
                    <button className="btn btn-primary" onClick={handleAddFolder} disabled={isRunning}>
                        Add
                    </button>
                </div>

                <div className="quick-paths">
                    {["C:\\Users", "D:\\", "E:\\", "F:\\"].map((p) => (
                        <button
                            key={p}
                            className="btn btn-ghost quick-path-btn"
                            onClick={() => {
                                if (!folders.includes(p)) {
                                    const updated = [...folders, p];
                                    setFolders(updated);
                                    localStorage.setItem("FindMyFile_indexed_folders", JSON.stringify(updated));
                                }
                            }}
                            disabled={isRunning}
                        >
                            {p}
                        </button>
                    ))}
                </div>

                {folders.length > 0 && (
                    <div className="folders-list">
                        {folders.map((f) => (
                            <div key={f} className="folder-item">
                                <span className="folder-icon">📁</span>
                                <span className="folder-path">{f}</span>
                                <button
                                    className="btn btn-ghost folder-remove"
                                    onClick={() => handleRemoveFolder(f)}
                                    disabled={isRunning}
                                >
                                    ✕
                                </button>
                            </div>
                        ))}
                    </div>
                )}

                {folders.length > 0 && !isRunning && (
                    <div className="folder-actions">
                        <button
                            className="btn btn-secondary"
                            onClick={handleScan}
                            disabled={isScanning}
                        >
                            {isScanning ? "Scanning..." : "🔍 Scan Files"}
                        </button>
                        {scanResult !== null && (
                            <span className="scan-count">
                                Found <strong>{scanResult.toLocaleString()}</strong> supported files
                            </span>
                        )}
                        <button
                            className="btn btn-primary btn-lg"
                            onClick={handleStartIndexing}
                            disabled={isStarting}
                        >
                            {isStarting ? "Starting..." : "🚀 Start Indexing"}
                        </button>
                    </div>
                )}
            </section>

            {/* Tips */}
            <section className="idx-section idx-tips">
                <h3>💡 Tips</h3>
                <ul>
                    <li>Incremental indexing: only <strong>new or modified</strong> files are processed.</li>
                    <li>Videos are automatically <strong>skipped</strong> (mp4, avi, mkv, etc.)</li>
                    <li>Face detection runs on each image — faces are stored for face search.</li>
                    <li>OCR extracts text from images so you can search for text in photos.</li>
                </ul>
            </section>
        </div>
    );
}
