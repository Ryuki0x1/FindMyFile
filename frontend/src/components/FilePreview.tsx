import { useState } from "react";
import type { SearchResult } from "../services/api";
import { getFileUrl } from "../services/api";
import "./FilePreview.css";

interface FilePreviewProps {
    file: SearchResult;
    onClose: () => void;
}

/** Returns the icon emoji for a file extension */
function docIcon(ext: string) {
    const e = ext.toLowerCase();
    if (e === ".pdf")  return "📄";
    if (e === ".docx" || e === ".doc") return "📝";
    if (e === ".pptx" || e === ".ppt") return "📊";
    if (e === ".xlsx" || e === ".xls") return "📋";
    if (e === ".txt" || e === ".md")   return "🗒️";
    if (e === ".csv")  return "📊";
    return "📁";
}

export default function FilePreview({ file, onClose }: FilePreviewProps) {
    const [copied, setCopied] = useState<"path" | "folder" | null>(null);
    const [iframeError, setIframeError] = useState(false);

    const ext = (file.extension || "").toLowerCase();
    const fileUrl = getFileUrl(file.filepath);

    // PDFs and plain text files can be embedded directly in the browser
    const isEmbeddable = ext === ".pdf" || ext === ".txt" || ext === ".md" || ext === ".csv";

    const copyText = async (text: string, type: "path" | "folder") => {
        await navigator.clipboard.writeText(text);
        setCopied(type);
        setTimeout(() => setCopied(null), 2000);
    };

    const handleCopyPath = () => copyText(file.filepath, "path");

    const handleCopyFolder = () => {
        // Works for both Windows (\) and Unix (/) paths
        const sep = file.filepath.includes("\\") ? "\\" : "/";
        const folder = file.filepath.substring(0, file.filepath.lastIndexOf(sep));
        copyText(folder, "folder");
    };

    const handleOpenInBrowser = () => {
        window.open(fileUrl, "_blank");
    };

    return (
        <div className="preview-overlay" onClick={onClose}>
            <div
                className={`preview-modal animate-slide-up ${isEmbeddable ? "preview-modal-wide" : ""}`}
                onClick={(e) => e.stopPropagation()}
            >
                <button className="preview-close" onClick={onClose} title="Close (Esc)">
                    ✕
                </button>

                {/* ── Preview area ── */}
                <div className={`preview-content ${isEmbeddable ? "preview-content-tall" : ""}`}>

                    {/* IMAGE */}
                    {file.file_type === "image" && (
                        <div className="preview-image-container">
                            <img
                                src={fileUrl}
                                alt={file.filename}
                                className="preview-image"
                                onError={(e) => {
                                    (e.target as HTMLImageElement).style.display = "none";
                                }}
                            />
                        </div>
                    )}

                    {/* PDF — embedded via iframe (browser built-in PDF viewer) */}
                    {file.file_type !== "image" && ext === ".pdf" && !iframeError && (
                        <iframe
                            src={fileUrl}
                            className="preview-pdf-frame"
                            title={file.filename}
                            onError={() => setIframeError(true)}
                        />
                    )}

                    {/* TXT / MD / CSV — embedded as plain text */}
                    {file.file_type !== "image" && (ext === ".txt" || ext === ".md" || ext === ".csv") && !iframeError && (
                        <iframe
                            src={fileUrl}
                            className="preview-pdf-frame preview-text-frame"
                            title={file.filename}
                            onError={() => setIframeError(true)}
                        />
                    )}

                    {/* OCR text preview for other documents OR iframe fallback */}
                    {file.file_type !== "image" && (!isEmbeddable || iframeError) && (
                        <div className="preview-doc-placeholder">
                            <span className="preview-doc-icon">{docIcon(file.extension)}</span>
                            <span className="preview-doc-ext">{file.extension.replace(".", "").toUpperCase()}</span>
                            {file.ocr_text ? (
                                <div className="preview-doc-text">
                                    <p className="preview-doc-text-label">Extracted text content:</p>
                                    <pre className="preview-doc-text-content">{file.ocr_text}</pre>
                                </div>
                            ) : (
                                <p className="preview-doc-hint">
                                    Click <strong>Open File</strong> to view in your default app
                                </p>
                            )}
                        </div>
                    )}
                </div>

                {/* ── Details panel ── */}
                <div className="preview-details">
                    <h3 className="preview-filename" title={file.filepath}>{file.filename}</h3>
                    <p className="preview-path">{file.filepath}</p>

                    <div className="preview-meta-grid">
                        {file.relevance_score > 0 && (
                            <div className="preview-meta-item">
                                <span className="preview-meta-label">Relevance</span>
                                <span className="preview-meta-value accent">{file.relevance_score}%</span>
                            </div>
                        )}
                        <div className="preview-meta-item">
                            <span className="preview-meta-label">Size</span>
                            <span className="preview-meta-value">{file.size_mb} MB</span>
                        </div>
                        <div className="preview-meta-item">
                            <span className="preview-meta-label">Type</span>
                            <span className="preview-meta-value">{file.extension}</span>
                        </div>
                        <div className="preview-meta-item">
                            <span className="preview-meta-label">Modified</span>
                            <span className="preview-meta-value">
                                {file.modified ? new Date(file.modified).toLocaleDateString() : "—"}
                            </span>
                        </div>
                        {file.date_taken && (
                            <div className="preview-meta-item">
                                <span className="preview-meta-label">Date Taken</span>
                                <span className="preview-meta-value">{file.date_taken}</span>
                            </div>
                        )}
                        {file.camera_model && (
                            <div className="preview-meta-item">
                                <span className="preview-meta-label">Camera</span>
                                <span className="preview-meta-value">{file.camera_model}</span>
                            </div>
                        )}
                        {file.match_type && (
                            <div className="preview-meta-item">
                                <span className="preview-meta-label">Match</span>
                                <span className="preview-meta-value">{file.match_type}</span>
                            </div>
                        )}
                    </div>

                    <div className="preview-actions">
                        <button
                            className="btn btn-primary"
                            onClick={handleOpenInBrowser}
                            title="Open file in a new browser tab"
                        >
                            🔗 Open File
                        </button>
                        <button
                            className="btn btn-secondary"
                            onClick={handleCopyPath}
                        >
                            {copied === "path" ? "✅ Copied!" : "📋 Copy Path"}
                        </button>
                        <button
                            className="btn btn-ghost"
                            onClick={handleCopyFolder}
                        >
                            {copied === "folder" ? "✅ Copied!" : "📂 Copy Folder"}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
