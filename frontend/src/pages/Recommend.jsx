import React, { useState } from 'react';
import { recommend, generateDescription } from '../api';
import '../App.css';

export default function Recommend() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadingDesc, setLoadingDesc] = useState({});
  const [error, setError] = useState("");

  const search = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setError("");
    try {
      const res = await recommend(query, 6);
      setResults(res?.data?.results || []);
      if (!res?.data?.results?.length) setError("Product not found. Try another title.");
    } catch {
      setError("Product not found or an error occurred. Try another title.");
    }
    setLoading(false);
  }

  const genDesc = async (uniq_id, i) => {
    setLoadingDesc(prev => ({ ...prev, [i]: true }));
    try {
      const res = await generateDescription(uniq_id);
      setResults(prev => prev.map((p, idx) => idx === i ? { ...p, gen: res.data.generated } : p));
    } finally {
      setLoadingDesc(prev => ({ ...prev, [i]: false }));
    }
  }

  return (
    <div className="recommend-container">
      <h2 className="recommend-title">Product Recommender</h2>

      <div className="search-wrapper">
        <input
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={e => e.key === "Enter" && search()}
          placeholder="Enter a product title..."
          className="search-input"
        />
        <button
          onClick={search}
          disabled={loading}
          className="search-button"
        >
          {loading ? "Searching..." : "Get Recommendations"}
        </button>
      </div>

      {error && <p className="error-message">{error}</p>}

      <div className="results-grid">
        {results.map((r, i) => (
          <div key={i} className="product-card">
            <h4 className="product-title">{r.title}</h4>
            <p className="product-category">Category: {r.categories}</p>
            <p className="product-price">Price: ${r.price}</p>
            <p className="product-description">{r.gen || (r.description?.slice(0, 100) + "...")}</p>
            <button
              onClick={() => genDesc(r.uniq_id, i)}
              disabled={loadingDesc[i]}
              className="generate-button"
            >
              {loadingDesc[i] ? "Generating..." : "Generate Description"}
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}