import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Campaigns from './pages/Campaigns';
import NewCampaign from './pages/NewCampaign';
import AdminPanel from './pages/Admin/AdminPanel';
import Layout from './components/Layout';

// Global CSS reset + theme
const globalStyle = `
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --bg:        #0a0f1c;
    --bg2:       linear-gradient(135deg, #1e215d 0%, #0d1117 100%);
    --bg3:       #181e2a;
    --border:    #232e47;
    --accent:    #00d4ff;
    --accent2:   #7c3aed;
    --accent3:   #ff5e62;
    --accent4:   #ffb347;
    --accent5:   #43e97b;
    --accent6:   #38f9d7;
    --green:     #00e88f;
    --red:       #ff4560;
    --yellow:    #ffd166;
    --pink:      #ff5ecf;
    --orange:    #ffb347;
    --lime:      #b6ff5e;
    --teal:      #38f9d7;
    --text:      #f3f6fb;
    --text2:     #a3b8d8;
    --text3:     #5a6b8a;
    --radius:    14px;
    --shadow:    0 4px 24px 0 rgba(0,0,0,0.12);
    --font-head: 'Syne', sans-serif;
    --font-body: 'DM Sans', sans-serif;
    --font-mono: 'DM Mono', monospace;
  }
  html, body { height: 100%; background: linear-gradient(120deg, #1e215d 0%, #0a0f1c 100%); color: var(--text); font-family: var(--font-body); }
  ::-webkit-scrollbar { width: 6px; } 
  ::-webkit-scrollbar-track { background: #1e215d; }
  ::-webkit-scrollbar-thumb { background: var(--accent2); border-radius: 3px; }
  button { cursor: pointer; font-family: var(--font-body); transition: box-shadow .2s, background .2s; }
  input, textarea, select { font-family: var(--font-body); }
  .vivid-gradient {
    background: linear-gradient(90deg, var(--accent2) 0%, var(--accent) 50%, var(--accent3) 100%);
    color: #fff;
    box-shadow: var(--shadow);
  }
  .vivid-card {
    background: linear-gradient(135deg, #232e47 0%, #181e2a 100%);
    box-shadow: var(--shadow);
    border-radius: var(--radius);
    border: 1px solid var(--accent2);
  }
  .vivid-btn {
    background: linear-gradient(90deg, var(--accent2) 0%, var(--accent) 100%);
    color: #fff;
    border: none;
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    font-weight: 700;
    letter-spacing: 0.5px;
    transition: background .2s, box-shadow .2s, transform .1s;
  }
  .vivid-btn:hover {
    background: linear-gradient(90deg, var(--accent3) 0%, var(--accent4) 100%);
    transform: translateY(-2px) scale(1.03);
    box-shadow: 0 8px 32px 0 rgba(0,0,0,0.18);
  }
  .vivid-status {
    background: linear-gradient(90deg, var(--green) 0%, var(--teal) 100%);
    color: #fff;
    border-radius: 8px;
    padding: 2px 10px;
    font-size: 12px;
    font-family: var(--font-mono);
    font-weight: 600;
    letter-spacing: 1px;
    box-shadow: 0 2px 8px 0 rgba(0,0,0,0.10);
  }
`;

function PrivateRoute({ children }) {
  const token = localStorage.getItem('access_token');
  return token ? children : <Navigate to="/login" replace />;
}

export default function App() {
  useEffect(() => {
    const style = document.createElement('style');
    style.textContent = globalStyle;
    document.head.appendChild(style);
    return () => document.head.removeChild(style);
  }, []);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<PrivateRoute><Layout /></PrivateRoute>}>
          <Route index element={<Dashboard />} />
          <Route path="campaigns" element={<Campaigns />} />
          <Route path="campaigns/new" element={<NewCampaign />} />
          <Route path="admin" element={<AdminPanel />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
