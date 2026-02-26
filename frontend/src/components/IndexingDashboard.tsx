import { useState, useEffect, useRef } from "react";
import { getIndexProgress, type IndexProgress } from "../services/api";
import "./IndexingDashboard.css";

interface IndexingDashboardProps {
    onDone?: () => void;
}

export default function IndexingDashboard({ onDone }: IndexingDashboardProps) {
    const [progress, setProgress] = useState<IndexProgress | null>(null);
    const intervalRef = useRef<ReturnType<typeof setInterval>>(undefined);

    useEffect(() => {
        // Poll progress every second
        const poll = async () => {
            try {
                const p = await getIndexProgress();
                setProgress(p);
                if (!p.is_running && p.total_files > 0 && p.processed > 0) {
                    clearInterval(intervalRef.current);
                    onDone?.();
                }
            } catch {
                // backend not reachable
            }
        };

        poll();
        intervalRef.current = setInterval(poll, 1000);

        return () => clearInterval(intervalRef.current);
    }, [onDone]);

    if (!progress) return null;

    const formatTime = (seconds: number) => {
        if (seconds < 60) return `${Math.round(seconds)}s`;
        if (seconds < 3600) return `${Math.floor(seconds / 60)}m ${Math.round(seconds % 60)}s`;
        return `${Math.floor(seconds / 3600)}h ${Math.floor((seconds % 3600) / 60)}m`;
    };

    if (!progress.is_running && progress.total_files === 0) return null;

    return (
        <div className="indexing-dashboard animate-in">
            <div className="indexing-header">
                <div className="indexing-status">
                    {progress.is_running ? (
                        <>
                            <div className="status-dot status-active" />
                            <span>Indexing in progress</span>
                        </>
                    ) : (
                        <>
                            <div className="status-dot status-done" />
                            <span>Indexing complete</span>
                        </>
                    )}
                </div>
                {progress.is_running && (
                    <span className="indexing-speed">
                        {progress.files_per_second} files/sec
                    </span>
                )}
            </div>

            <div className="progress-bar">
                <div
                    className="progress-bar-fill"
                    style={{ width: `${progress.percent_complete}%` }}
                />
            </div>

            <div className="indexing-stats">
                <div className="indexing-stat">
                    <span className="indexing-stat-value">{progress.processed.toLocaleString()}</span>
                    <span className="indexing-stat-label">Processed</span>
                </div>
                <div className="indexing-stat">
                    <span className="indexing-stat-value">{progress.skipped.toLocaleString()}</span>
                    <span className="indexing-stat-label">Skipped</span>
                </div>
                <div className="indexing-stat">
                    <span className="indexing-stat-value">
                        {progress.total_files.toLocaleString()}
                    </span>
                    <span className="indexing-stat-label">Total</span>
                </div>
                {progress.is_running && (
                    <div className="indexing-stat">
                        <span className="indexing-stat-value">
                            {formatTime(progress.eta_seconds)}
                        </span>
                        <span className="indexing-stat-label">ETA</span>
                    </div>
                )}
                {!progress.is_running && progress.elapsed_seconds > 0 && (
                    <div className="indexing-stat">
                        <span className="indexing-stat-value">
                            {formatTime(progress.elapsed_seconds)}
                        </span>
                        <span className="indexing-stat-label">Elapsed</span>
                    </div>
                )}
            </div>

            {progress.is_running && progress.current_file && (
                <p className="indexing-current" title={progress.current_file}>
                    {progress.current_file}
                </p>
            )}

            {progress.error_count > 0 && (
                <p className="indexing-errors">
                    ⚠️ {progress.error_count} error(s) during indexing
                </p>
            )}
        </div>
    );
}
