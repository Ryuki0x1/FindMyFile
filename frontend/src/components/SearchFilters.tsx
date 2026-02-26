import { useState } from "react";
import "./SearchFilters.css";

export interface FilterState {
  fileType: string;
  folderPath: string;
  minScore: number;
  extension: string;
}

interface SearchFiltersProps {
  filters: FilterState;
  onChange: (filters: FilterState) => void;
  onReset: () => void;
  disabled?: boolean;
}

export default function SearchFilters({ filters, onChange, onReset, disabled }: SearchFiltersProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const handleChange = (key: keyof FilterState, value: string | number) => {
    onChange({ ...filters, [key]: value });
  };

  const hasActiveFilters = 
    filters.fileType !== "" || 
    filters.folderPath !== "" || 
    filters.minScore > 0 || 
    filters.extension !== "";

  return (
    <div className="search-filters">
      <button
        className={`filters-toggle ${isExpanded ? "active" : ""} ${hasActiveFilters ? "has-filters" : ""}`}
        onClick={() => setIsExpanded(!isExpanded)}
        disabled={disabled}
      >
        <svg className="filter-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M3 6h18M7 12h10M10 18h4" />
        </svg>
        <span>Filters</span>
        {hasActiveFilters && <span className="filter-badge">{
          [filters.fileType, filters.folderPath, filters.minScore > 0, filters.extension].filter(Boolean).length
        }</span>}
        <svg className={`chevron ${isExpanded ? "up" : "down"}`} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {isExpanded && (
        <div className="filters-panel">
          <div className="filters-grid">
            {/* File Type Filter */}
            <div className="filter-group">
              <label htmlFor="file-type-filter">File Type</label>
              <select
                id="file-type-filter"
                value={filters.fileType}
                onChange={(e) => handleChange("fileType", e.target.value)}
                className="filter-select"
                disabled={disabled}
              >
                <option value="">All Files</option>
                <option value="image">Images Only</option>
                <option value="document">Documents Only</option>
              </select>
            </div>

            {/* Extension Filter */}
            <div className="filter-group">
              <label htmlFor="extension-filter">Extension</label>
              <select
                id="extension-filter"
                value={filters.extension}
                onChange={(e) => handleChange("extension", e.target.value)}
                className="filter-select"
                disabled={disabled}
              >
                <option value="">Any</option>
                <optgroup label="Images">
                  <option value=".jpg">.jpg</option>
                  <option value=".png">.png</option>
                  <option value=".gif">.gif</option>
                  <option value=".webp">.webp</option>
                  <option value=".bmp">.bmp</option>
                </optgroup>
                <optgroup label="Documents">
                  <option value=".pdf">.pdf</option>
                  <option value=".docx">.docx</option>
                  <option value=".txt">.txt</option>
                  <option value=".xlsx">.xlsx</option>
                </optgroup>
              </select>
            </div>

            {/* Folder Path Filter */}
            <div className="filter-group full-width">
              <label htmlFor="folder-filter">
                Folder Path 
                <span className="filter-hint">(search only in specific folder)</span>
              </label>
              <input
                id="folder-filter"
                type="text"
                value={filters.folderPath}
                onChange={(e) => handleChange("folderPath", e.target.value)}
                placeholder="e.g., D:\Photos\2024 or /home/user/photos"
                className="filter-input"
                disabled={disabled}
              />
              {filters.folderPath && (
                <p className="filter-info">
                  ⚡ Searching only in: <code>{filters.folderPath}</code>
                </p>
              )}
            </div>

            {/* Minimum Score Filter */}
            <div className="filter-group full-width">
              <label htmlFor="score-filter">
                Minimum Relevance Score: <strong>{filters.minScore}%</strong>
                <span className="filter-hint">(filter out low-quality matches)</span>
              </label>
              <div className="slider-container">
                <input
                  id="score-filter"
                  type="range"
                  min="0"
                  max="100"
                  step="5"
                  value={filters.minScore}
                  onChange={(e) => handleChange("minScore", parseInt(e.target.value))}
                  className="filter-slider"
                  disabled={disabled}
                />
                <div className="slider-labels">
                  <span>0% (Show all)</span>
                  <span>50% (Balanced)</span>
                  <span>100% (Perfect only)</span>
                </div>
              </div>
              {filters.minScore > 0 && (
                <p className="filter-info">
                  ✅ Only showing results with {filters.minScore}%+ relevance
                </p>
              )}
            </div>
          </div>

          {hasActiveFilters && (
            <div className="filters-actions">
              <button className="reset-filters-btn" onClick={onReset} disabled={disabled}>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8" />
                  <path d="M21 3v5h-5M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16" />
                  <path d="M3 21v-5h5" />
                </svg>
                Reset Filters
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
