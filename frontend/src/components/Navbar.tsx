import { useNavigate, useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import { healthCheck, getSearchStats, getIndexProgress } from "../services/api";
import "./Navbar.css";

export default function Navbar() {
    const navigate = useNavigate();
    const location = useLocation();
    const [backendReady, setBackendReady] = useState(false);
    const [totalIndexed, setTotalIndexed] = useState(0);
    const [isIndexing, setIsIndexing] = useState(false);

    useEffect(() => {
        const check = async () => {
            const ok = await healthCheck();
            setBackendReady(ok);
            if (ok) {
                try {
                    const stats = await getSearchStats();
                    setTotalIndexed(stats.total_files);
                    const prog = await getIndexProgress();
                    setIsIndexing(prog.is_running);
                } catch { /* ignore */ }
            }
        };
        check();
        const interval = setInterval(check, 5000);
        return () => clearInterval(interval);
    }, []);

    const isActive = (path: string) => location.pathname === path;

    return (
        <header className="navbar">
            <div className="navbar-left">
                <button className="navbar-logo" onClick={() => navigate("/")} title="Home">
                    <span className="logo-icon">🖼️</span>
                    <h1 className="logo-text">
                        Find<span className="gradient-text">My</span>Pic
                    </h1>
                </button>
            </div>

            <nav className="navbar-center">
                <button
                    className={`nav-link ${isActive("/") ? "active" : ""}`}
                    onClick={() => navigate("/")}
                >
                    <span className="nav-icon">🔍</span>
                    <span>Search</span>
                </button>
                <button
                    className={`nav-link ${isActive("/indexing") ? "active" : ""}`}
                    onClick={() => navigate("/indexing")}
                >
                    <span className="nav-icon">📊</span>
                    <span>Indexing</span>
                    {isIndexing && <span className="nav-badge pulse-badge" />}
                </button>
                <button
                    className={`nav-link ${isActive("/settings") ? "active" : ""}`}
                    onClick={() => navigate("/settings")}
                >
                    <span className="nav-icon">⚙️</span>
                    <span>Settings</span>
                </button>
            </nav>

            <div className="navbar-right">
                <div className="index-count" title={`${totalIndexed} files indexed`}>
                    <span className="count-icon">📁</span>
                    <span className="count-value">{totalIndexed.toLocaleString()}</span>
                </div>
                <div className={`conn-status ${backendReady ? "online" : "offline"}`}>
                    <div className="conn-dot" />
                    <span>{backendReady ? "Online" : "Offline"}</span>
                </div>
            </div>
        </header>
    );
}
