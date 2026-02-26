import { useState, useEffect } from "react";
import { getSystemInfo, startIndexing, scanFiles, type SystemInfo } from "../services/api";
import "./Onboarding.css";

interface OnboardingProps {
    onComplete: () => void;
}

type Step = "welcome" | "hardware" | "folders" | "indexing";

export default function Onboarding({ onComplete }: OnboardingProps) {
    const [step, setStep] = useState<Step>("welcome");
    const [systemInfo, setSystemInfo] = useState<SystemInfo | null>(null);
    const [folderPath, setFolderPath] = useState("");
    const [folders, setFolders] = useState<string[]>([]);
    const [scanResult, setScanResult] = useState<{ total: number } | null>(null);
    const [isScanning, setIsScanning] = useState(false);
    const [isStarting, setIsStarting] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        if (step === "hardware") {
            getSystemInfo()
                .then(setSystemInfo)
                .catch(() => setError("Could not connect to backend. Is it running?"));
        }
    }, [step]);

    const handleAddFolder = () => {
        const path = folderPath.trim();
        if (path && !folders.includes(path)) {
            setFolders([...folders, path]);
            setFolderPath("");
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
            setScanResult({ total: result.total_files });
        } catch (err: any) {
            setError(err.message || "Failed to scan folders. Check that paths exist and are accessible.");
        }
        setIsScanning(false);
    };

    const handleStartIndexing = async () => {
        setIsStarting(true);
        setError("");
        try {
            await startIndexing(folders);
            localStorage.setItem("findmypic_setup_done", "true");
            localStorage.setItem("findmypic_indexed_folders", JSON.stringify(folders));
            onComplete();
        } catch (err: any) {
            setError(err.message || "Failed to start indexing. Check that paths exist and are accessible.");
            setIsStarting(false);
        }
    };

    return (
        <div className="onboarding-overlay">
            <div className="onboarding-container animate-slide-up">
                {/* Step 1: Welcome */}
                {step === "welcome" && (
                    <div className="onboarding-step">
                        <div className="onboarding-logo">🖼️</div>
                        <h1 className="onboarding-title">
                            Welcome to <span className="gradient-text">FindMyPic</span>
                        </h1>
                        <p className="onboarding-subtitle">
                            Find any photo or document on your PC by describing it.
                        </p>
                        <div className="onboarding-features">
                            <div className="feature-pill">🔒 100% Local</div>
                            <div className="feature-pill">🚫 No Cloud</div>
                            <div className="feature-pill">⚡ AI-Powered</div>
                            <div className="feature-pill">🎯 GPU Optimized</div>
                        </div>
                        <button
                            className="btn btn-primary btn-lg"
                            onClick={() => setStep("hardware")}
                        >
                            Get Started →
                        </button>
                    </div>
                )}

                {/* Step 2: Hardware Detection */}
                {step === "hardware" && (
                    <div className="onboarding-step">
                        <h2 className="onboarding-step-title">⚙️ Hardware Detection</h2>
                        <p className="onboarding-step-desc">
                            We detected your hardware and picked the best AI models for it.
                        </p>

                        {error && <div className="onboarding-error">{error}</div>}

                        {systemInfo ? (
                            <div className="hardware-info">
                                <div className="hardware-card">
                                    <div className="hardware-row">
                                        <span className="hardware-label">GPU</span>
                                        <span className="hardware-value">{systemInfo.gpu.name}</span>
                                    </div>
                                    <div className="hardware-row">
                                        <span className="hardware-label">VRAM</span>
                                        <span className="hardware-value">{systemInfo.gpu.vram_gb} GB</span>
                                    </div>
                                    <div className="hardware-row">
                                        <span className="hardware-label">CUDA</span>
                                        <span className="hardware-value">
                                            {systemInfo.gpu.cuda_available ? (
                                                <span className="badge badge-success">Available</span>
                                            ) : (
                                                <span className="badge badge-warning">Not Available</span>
                                            )}
                                        </span>
                                    </div>
                                    <div className="hardware-row">
                                        <span className="hardware-label">RAM</span>
                                        <span className="hardware-value">{systemInfo.system.ram_gb} GB</span>
                                    </div>
                                </div>

                                <div className="tier-recommendation">
                                    <div className="tier-badge">Tier {systemInfo.recommendation.tier}</div>
                                    <h3>{systemInfo.recommendation.tier_name}</h3>
                                    <p>{systemInfo.recommendation.description}</p>
                                    <div className="tier-details">
                                        <div>
                                            <span className="tier-detail-label">Speed</span>
                                            <span>{systemInfo.recommendation.estimated_speed}</span>
                                        </div>
                                        <div>
                                            <span className="tier-detail-label">Download</span>
                                            <span>{(systemInfo.recommendation.total_download_mb / 1024).toFixed(1)} GB</span>
                                        </div>
                                    </div>
                                </div>

                                <button
                                    className="btn btn-primary btn-lg"
                                    onClick={() => setStep("folders")}
                                >
                                    Continue →
                                </button>
                            </div>
                        ) : (
                            !error && (
                                <div className="hardware-loading">
                                    <div className="search-spinner" style={{ width: 32, height: 32 }} />
                                    <p>Detecting hardware...</p>
                                </div>
                            )
                        )}
                    </div>
                )}

                {/* Step 3: Folder Selection */}
                {step === "folders" && (
                    <div className="onboarding-step">
                        <h2 className="onboarding-step-title">📂 Choose Folders</h2>
                        <p className="onboarding-step-desc">
                            Select which folders to index. You can add more later in Settings.
                        </p>

                        <div className="folder-input-row">
                            <input
                                type="text"
                                className="input"
                                placeholder="Enter folder path (e.g., D:\Photos)"
                                value={folderPath}
                                onChange={(e) => setFolderPath(e.target.value)}
                                onKeyDown={(e) => e.key === "Enter" && handleAddFolder()}
                            />
                            <button className="btn btn-primary" onClick={handleAddFolder}>
                                Add
                            </button>
                        </div>

                        <div className="quick-add">
                            <span className="quick-add-label">Quick add:</span>
                            {["C:\\Users", "D:\\", "E:\\"].map((p) => (
                                <button
                                    key={p}
                                    className="btn btn-ghost"
                                    onClick={() => {
                                        if (!folders.includes(p)) setFolders([...folders, p]);
                                    }}
                                >
                                    {p}
                                </button>
                            ))}
                        </div>

                        {error && <div className="onboarding-error">{error}</div>}

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
                                    {isScanning ? "Scanning..." : "Scan Files"}
                                </button>

                                {scanResult && (
                                    <span className="scan-result">
                                        Found <strong>{scanResult.total.toLocaleString()}</strong> files
                                    </span>
                                )}

                                <button
                                    className="btn btn-primary btn-lg"
                                    onClick={handleStartIndexing}
                                    disabled={isStarting}
                                >
                                    {isStarting ? "Starting..." : "Start Indexing →"}
                                </button>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}
