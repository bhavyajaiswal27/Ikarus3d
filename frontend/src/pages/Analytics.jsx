import React, { useEffect, useState } from 'react';
import { getAnalytics } from '../api';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import '../App.css';

export default function Analytics() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await getAnalytics();
        setStats(res.data);
      } catch {
        setStats({ error: 'Failed to load analytics.' });
      }
    };
    fetchData();
  }, []);

  if (!stats) return <div className="loading">Loading analytics...</div>;
  if (stats.error) return <div className="error">{stats.error}</div>;

  const catData = Object.entries(stats.top_categories || {}).map(([k, v]) => ({ category: k, count: v }));
  const brandData = Object.entries(stats.top_brands || {}).map(([k, v]) => ({ brand: k, count: v }));

  return (
    <div className="analytics-container">
      <h2 className="analytics-title">Dataset Analytics</h2>

      <div className="stats-summary">
        <p className="stat-item">
          Total Products: <span className="stat-value stat-blue">{stats.count || 0}</span>
        </p>
        <p className="stat-item">
          Average Price: <span className="stat-value stat-green">${stats.price_mean ? stats.price_mean.toFixed(2) : 'N/A'}</span>
        </p>
      </div>

      <div className="chart-section">
        <h3 className="chart-title">Top Categories</h3>
        <div className="chart-container">
          {catData.length === 0 ? (
            <p className="no-data">No category data available.</p>
          ) : (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={catData}>
                <XAxis dataKey="category" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#3b82f6" radius={[5,5,0,0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      <div className="chart-section">
        <h3 className="chart-title">Top Brands</h3>
        <div className="chart-container">
          {brandData.length === 0 ? (
            <p className="no-data">No brand data available.</p>
          ) : (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={brandData}>
                <XAxis dataKey="brand" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#10b981" radius={[5,5,0,0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>
    </div>
  );
}