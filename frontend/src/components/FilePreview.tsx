import type { SearchResult } from "../services/api";
import { getFileUrl } from "../services/api";
import "./FilePreview.css";

interface FilePreviewProps {
    file: SearchResult;
    onClose: () => void;
}

export default function FilePreview({ file, onClose }: FilePreviewProps) {
    const handleOpenFile = () => {
        // In Electron, this would use shell.openPath
        // For web dev, we just show the path
        navigator.clipboard.writeText(file.filepath);
    };

    const handleOpenFolder = () => {
        const folder = file.filepath.substring(0, file.filepath.lastIndexOf("\\"));
        navigator.clipboard.writeText(folder);
    };

    return (
        <div className="preview-overlay" onClick={onClose}>
            <div className="preview-modal animate-slide-up" onClick={(e) => e.stopPropagation()}>
                <button className="preview-close" onClick={onClose}>
                    ✕
                </button>

                <div className="preview-content">
                    {file.file_type === "image" ? (
                        <div className="preview-image-container">
                            <img
                                src={getFileUrl(file.filepath)}
                                alt={file.filename}
                                className="preview-image"
                                onError={(e) => {
                                    (e.target as HTMLImageElement).style.display = "none";
                                }}
                            />
                        </div>
                    ) : (
                        <div className="preview-doc-placeholder">
                            <span className="preview-doc-ext">{file.extension}</span>
                            <p>Document Preview</p>
                        </div>
                    )}
                </div>

                <div className="preview-details">
                    <h3 className="preview-filename">{file.filename}</h3>
                    <p className="preview-path">{file.filepath}</p>

                    <div className="preview-meta-grid">
                        <div className="preview-meta-item">
                            <span className="preview-meta-label">Relevance</span>
                            <span className="preview-meta-value accent">{file.relevance_score}%</span>
                        </div>
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
                                {new Date(file.modified).toLocaleDateString()}
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
                    </div>

                    <div className="preview-actions">
                        <button className="btn btn-primary" onClick={handleOpenFile}>
                            📋 Copy Path
                        </button>
                        <button className="btn btn-secondary" onClick={handleOpenFolder}>
                            📂 Copy Folder Path
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
