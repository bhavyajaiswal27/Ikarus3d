import React from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from "react-router-dom";
import Recommend from './pages/Recommend';
import Analytics from './pages/Analytics';
import './App.css';

function App() {
  return (
    <Router>
      {/* Navigation */}
      <nav className="navbar">
        <NavLink
          to="/"
          className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}
        >
          Recommend
        </NavLink>
        <NavLink
          to="/analytics"
          className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}
        >
          Analytics
        </NavLink>
      </nav>

      {/* Page Container */}
      <div className="page-container">
        <Routes>
          <Route path="/" element={<Recommend />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="*" element={<div className="not-found">Page Not Found</div>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;