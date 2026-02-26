import { useState, useEffect, useCallback } from "react";
import { Routes, Route, useNavigate, useLocation } from "react-router-dom";
import Navbar from "./components/Navbar";
import Onboarding from "./components/Onboarding";
import SearchPage from "./pages/SearchPage";
import IndexingPage from "./pages/IndexingPage";
import SettingsPage from "./pages/SettingsPage";
import { healthCheck, getSearchStats } from "./services/api";
import "./App.css";

function App() {
  const navigate = useNavigate();
  const location = useLocation();
  const [setupDone, setSetupDone] = useState(() => {
    return !!localStorage.getItem("FindMyFile_setup_done");
  });
  const [totalIndexed, setTotalIndexed] = useState(0);
  const [backendReady, setBackendReady] = useState(false);

  // Check backend and load stats
  useEffect(() => {
    const check = async () => {
      const ok = await healthCheck();
      setBackendReady(ok);
      if (ok) {
        try {
          const stats = await getSearchStats();
          setTotalIndexed(stats.total_files);
        } catch { /* ignore */ }
      }
    };
    check();
    const interval = setInterval(check, 10000);
    return () => clearInterval(interval);
  }, []);

  const handleOnboardingComplete = useCallback(() => {
    setSetupDone(true);
    getSearchStats()
      .then((s) => setTotalIndexed(s.total_files))
      .catch(() => { });
    navigate("/");
  }, [navigate]);

  // Show onboarding if first time
  if (!setupDone) {
    return <Onboarding onComplete={handleOnboardingComplete} />;
  }

  // Show onboarding route if navigated to /setup
  const isSetupRoute = location.pathname === "/setup";
  if (isSetupRoute) {
    return (
      <Onboarding
        onComplete={() => {
          setSetupDone(true);
          navigate("/");
        }}
      />
    );
  }

  return (
    <div className="app">
      <Navbar />

      {!backendReady && (
        <div className="backend-warning animate-in">
          <p>⚠️ Backend is not running. Start it with:</p>
          <code>cd backend; .venv\Scripts\python.exe -m app.main</code>
        </div>
      )}

      <main className="app-main">
        <Routes>
          <Route path="/" element={<SearchPage totalIndexed={totalIndexed} />} />
          <Route path="/dashboard" element={<SearchPage totalIndexed={totalIndexed} />} />
          <Route path="/indexing" element={<IndexingPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
