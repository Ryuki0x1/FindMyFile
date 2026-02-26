import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
    getSettings,
    clearIndex,
    startIndexing,
    scanFiles,
    type AppSettings,
} from "../services/api";
import "./SettingsPage.css";

export default function SettingsPage() {
    const navigate = useNavigate();
    const [settings, setSettings] = useState<AppSettings | null>(null);
    const [folders, setFolders] = useState<string[]>([]);
    const [newFolder, setNewFolder] = useState("");
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const [isClearing, setIsClearing] = useState(false);
    const [isScanning, setIsScanning] = useState(false);
    const [scanResult, setScanResult] = useState<number | null>(null);

    useEffect(() => {
        loadSettings();
    }, []);

    const loadSettings = async () => {
        try {
            const s = await getSettings();
            setSettings(s);
            setFolders(s.indexed_folders || []);
        } catch {
            setError("Could not load settings. Is the backend running?");
        }
    };

    const handleAddFolder = () => {
        const path = newFolder.trim();
        if (path && !folders.includes(path)) {
            setFolders([...folders, path]);
            setNewFolder("");
            setError("");
        }
    };

    const handleRemoveFolder = (path: string) => {
        setFolders(folders.filter((f) => f !== path));
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
        setError("");
        try {
            await startIndexing(folders);
            localStorage.setItem("findmypic_indexed_folders", JSON.stringify(folders));
            setSuccess("Indexing started! Go to the Indexing page to monitor progress.");
            navigate("/indexing");
        } catch (err: any) {
            setError(err.message || "Failed to start indexing.");
        }
    };

    const handleClearIndex = async () => {
        if (!confirm("⚠️ This will delete ALL indexed data (embeddings, faces, thumbnails). Are you sure?"))
            return;
        setIsClearing(true);
        setError("");
        try {
            await clearIndex();
            setSuccess("Index cleared successfully.");
            loadSettings();
        } catch (err: any) {
            setError(err.message || "Failed to clear index.");
        }
        setIsClearing(false);
    };

    const handleResetOnboarding = () => {
        localStorage.removeItem("findmypic_setup_done");
        localStorage.removeItem("findmypic_indexed_folders");
        navigate("/");
        window.location.reload();
    };

    return (
        <div className="settings-page animate-in">
            <div className="page-header">
                <button className="btn btn-ghost back-btn" onClick={() => navigate(-1)}>
                    ← Back
                </button>
                <h1 className="page-title">
                    <span className="page-icon">⚙️</span> Settings
                </h1>
            </div>

            {error && <div className="settings-alert alert-error">{error}</div>}
            {success && <div className="settings-alert alert-success">{success}</div>}

            {/* Indexed Folders Section */}
            <section className="settings-section">
                <h2 className="section-title">📂 Indexed Folders</h2>
                <p className="section-desc">
                    Choose which folders to scan and index. You can add multiple paths.
                </p>

                <div className="folder-input-row">
                    <input
                        type="text"
                        className="input"
                        placeholder="Enter folder path (e.g., E:\Photos)"
                        value={newFolder}
                        onChange={(e) => setNewFolder(e.target.value)}
                        onKeyDown={(e) => e.key === "Enter" && handleAddFolder()}
                    />
                    <button className="btn btn-primary" onClick={handleAddFolder}>
                        Add
                    </button>
                </div>

                <div className="quick-paths">
                    {["C:\\Users", "D:\\", "E:\\", "F:\\"].map((p) => (
                        <button
                            key={p}
                            className="btn btn-ghost quick-path-btn"
                            onClick={() => {
                                if (!folders.includes(p)) setFolders([...folders, p]);
                            }}
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
                                >
                                    ✕
                                </button>
                            </div>
                        ))}
                    </div>
                )}

                {folders.length > 0 && (
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
                        >
                            🚀 Start Indexing
                        </button>
                    </div>
                )}
            </section>

            {/* Index Info Section */}
            <section className="settings-section">
                <h2 className="section-title">💾 Index Storage</h2>
                {settings && (
                    <div className="info-grid">
                        <div className="info-card">
                            <span className="info-label">Total Indexed Files</span>
                            <span className="info-value">{settings.total_indexed_files.toLocaleString()}</span>
                        </div>
                        <div className="info-card">
                            <span className="info-label">Data Directory</span>
                            <span className="info-value info-path">{(settings as any).data_dir || "default"}</span>
                        </div>
                        <div className="info-card">
                            <span className="info-label">ChromaDB</span>
                            <span className="info-value info-path">{(settings as any).chroma_dir || "default"}</span>
                        </div>
                        <div className="info-card">
                            <span className="info-label">Thumbnails</span>
                            <span className="info-value info-path">{(settings as any).thumbnails_dir || "default"}</span>
                        </div>
                    </div>
                )}
                <p className="settings-hint">
                    💡 The <code>data/</code> folder is portable — you can copy it to another machine or backup drive.
                    Set <code>FINDMYPIC_DATA_DIR</code> environment variable to change its location.
                </p>
            </section>

            {/* Supported Formats */}
            <section className="settings-section">
                <h2 className="section-title">📋 Supported Formats</h2>
                {settings && (
                    <div className="formats-grid">
                        <div className="format-group">
                            <h3>📸 Images ({settings.image_extensions.length} formats)</h3>
                            <div className="format-tags">
                                {settings.image_extensions.map((ext) => (
                                    <span key={ext} className="format-tag">{ext}</span>
                                ))}
                            </div>
                        </div>
                        <div className="format-group">
                            <h3>📄 Documents ({settings.document_extensions.length} formats)</h3>
                            <div className="format-tags">
                                {settings.document_extensions.map((ext) => (
                                    <span key={ext} className="format-tag">{ext}</span>
                                ))}
                            </div>
                        </div>
                        <div className="format-group">
                            <h3>🚫 Videos (excluded)</h3>
                            <div className="format-tags">
                                {((settings as any).video_extensions_excluded || []).map((ext: string) => (
                                    <span key={ext} className="format-tag format-tag-excluded">{ext}</span>
                                ))}
                            </div>
                        </div>
                    </div>
                )}
            </section>

            {/* Danger Zone */}
            <section className="settings-section danger-zone">
                <h2 className="section-title">⚠️ Danger Zone</h2>
                <div className="danger-actions">
                    <div className="danger-item">
                        <div>
                            <strong>Clear Index</strong>
                            <p>Delete all indexed data — embeddings, face data, thumbnails. You'll need to re-index.</p>
                        </div>
                        <button
                            className="btn btn-danger"
                            onClick={handleClearIndex}
                            disabled={isClearing}
                        >
                            {isClearing ? "Clearing..." : "🗑️ Clear All Data"}
                        </button>
                    </div>
                    <div className="danger-item">
                        <div>
                            <strong>Re-run Setup</strong>
                            <p>Go back to the onboarding wizard to reconfigure everything from scratch.</p>
                        </div>
                        <button className="btn btn-danger" onClick={handleResetOnboarding}>
                            🔄 Reset Setup
                        </button>
                    </div>
                </div>
            </section>
        </div>
    );
}
