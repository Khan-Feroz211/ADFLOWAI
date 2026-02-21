import React, { useState } from 'react';
import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import { authAPI } from '../services/api';

const s = {
  shell:   { display:'flex', height:'100vh', overflow:'hidden', background: 'linear-gradient(120deg, #1e215d 0%, #0a0f1c 100%)' },
  sidebar: {
    width: 240, minWidth: 240,
    background: 'linear-gradient(135deg, #232e47 0%, #181e2a 100%)',
    borderRight: '2px solid var(--accent2)',
    display: 'flex', flexDirection: 'column', padding: '24px 0',
    boxShadow: '0 0 32px 0 rgba(60,40,120,0.18)',
  },
  logo: {
    padding: '0 24px 32px', fontFamily: 'var(--font-head)',
    fontSize: 24, fontWeight: 900, letterSpacing: '-0.5px',
    color: 'var(--accent)',
    textShadow: '0 2px 12px var(--accent2)',
  },
  logoSub: { fontSize: 11, color: 'var(--accent4)', fontFamily: 'var(--font-mono)', letterSpacing: 2, display:'block', marginTop: 2 },
  nav:     { flex: 1, display: 'flex', flexDirection: 'column', gap: 4, padding: '0 12px' },
  link: (active) => ({
    display: 'flex', alignItems: 'center', gap: 12, padding: '12px 16px',
    borderRadius: 10, textDecoration: 'none', fontSize: 15, fontWeight: 600,
    color: active ? 'var(--accent3)' : 'var(--text2)',
    background: active ? 'linear-gradient(90deg, var(--accent2) 0%, var(--accent) 100%)' : 'transparent',
    borderLeft: active ? '4px solid var(--accent3)' : '4px solid transparent',
    boxShadow: active ? '0 2px 12px 0 var(--accent2)33' : 'none',
    transition: 'all .18s',
  }),
  section: { fontSize: 11, fontFamily: 'var(--font-mono)', color: 'var(--accent4)', letterSpacing: 2, padding: '16px 26px 6px', textTransform: 'uppercase', fontWeight: 700 },
  bottom:  { padding: '18px 14px', borderTop: '2px solid var(--accent2)', marginTop: 'auto', background: 'linear-gradient(90deg, #1e215d 0%, #181e2a 100%)' },
  user:    { display:'flex', alignItems:'center', gap: 12, padding: '10px 16px', borderRadius: 10, background: 'linear-gradient(90deg, var(--accent5) 0%, var(--accent6) 100%)', boxShadow: '0 2px 8px 0 rgba(0,232,143,0.10)' },
  avatar:  { width: 36, height: 36, borderRadius: '50%', background: 'linear-gradient(135deg,var(--accent2),var(--accent3))', display:'flex', alignItems:'center', justifyContent:'center', fontSize: 16, fontWeight: 900, color:'#fff', flexShrink: 0, boxShadow: '0 2px 8px 0 var(--accent2)33' },
  userName:{ fontSize: 15, fontWeight: 700, color: 'var(--text)' },
  userRole:{ fontSize: 12, color: 'var(--accent4)', fontFamily: 'var(--font-mono)', fontWeight: 600 },
  logoutBtn:{ width:'100%', marginTop: 10, padding: '10px', background:'linear-gradient(90deg, var(--accent3) 0%, var(--accent4) 100%)', border:'none', borderRadius: 10, color:'#fff', fontSize: 14, fontWeight: 700, boxShadow: '0 2px 8px 0 var(--accent3)33', transition:'all .15s' },
  main:    { flex: 1, overflow: 'auto', background: 'transparent' },
};

const navItems = [
  { to: '/',          icon: '▦', label: 'Dashboard' },
  { to: '/campaigns', icon: '◈', label: 'Campaigns' },
];

const adminNavItems = [
  { to: '/admin', icon: '⚙', label: 'Admin Panel' },
];

export default function Layout() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem('user') || '{}');

  const downloadReport = async (fmt) => {
    try {
      const token = localStorage.getItem('access_token');
      const res = await fetch(`/api/v1/reports/campaigns?format=${fmt}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      const blob = await res.blob();
      const url  = URL.createObjectURL(blob);
      const a    = document.createElement('a');
      a.href     = url;
      a.download = `adflowai_report.${fmt}`;
      a.click();
      URL.revokeObjectURL(url);
    } catch {}
  };

  const logout = async () => {
    try { await authAPI.logout(); } catch {}
    localStorage.clear();
    navigate('/login');
  };

  return (
    <div style={s.shell}>
      <aside style={s.sidebar}>
        <div style={s.logo}>
          ADFLOW<span style={{ color: 'var(--text2)' }}>AI</span>
          <span style={s.logoSub}>AI CAMPAIGN OPTIMIZER</span>
        </div>

        <span style={s.section}>Navigation</span>
        <nav style={s.nav}>
          {navItems.map(({ to, icon, label }) => (
            <NavLink key={to} to={to} end={to==='/'} style={({ isActive }) => s.link(isActive)}>
              <span style={{ fontSize: 16 }}>{icon}</span>
              {label}
            </NavLink>
          ))}
        </nav>

        <span style={s.section}>Quick Actions</span>
        <nav style={{ padding: '0 12px', display:'flex', flexDirection:'column', gap:4 }}>
          <NavLink to="/campaigns/new" style={({ isActive }) => s.link(isActive)}>
            <span style={{ fontSize: 16 }}>＋</span>
            New Campaign
          </NavLink>
          <button onClick={() => downloadReport('csv')} style={{ ...s.link(false), border:'none', cursor:'pointer', width:'100%', textAlign:'left' }}>
            <span style={{ fontSize: 14 }}>↓</span>
            Export CSV
          </button>
          <button onClick={() => downloadReport('html')} style={{ ...s.link(false), border:'none', cursor:'pointer', width:'100%', textAlign:'left' }}>
            <span style={{ fontSize: 14 }}>↓</span>
            Export Report
          </button>
        </nav>

        {user.role === 'admin' && (
          <>
            <span style={s.section}>Admin</span>
            <nav style={{ padding: '0 12px' }}>
              {adminNavItems.map(({ to, icon, label }) => (
                <NavLink key={to} to={to} style={({ isActive }) => s.link(isActive)}>
                  <span style={{ fontSize: 16 }}>{icon}</span>
                  {label}
                </NavLink>
              ))}
            </nav>
          </>
        )}

        <div style={s.bottom}>
          <div style={s.user}>
            <div style={s.avatar}>{(user.username || 'U')[0].toUpperCase()}</div>
            <div>
              <div style={s.userName}>{user.username || 'User'}</div>
              <div style={s.userRole}>{user.role || 'user'}</div>
            </div>
          </div>
          <button style={s.logoutBtn} onClick={logout}>Sign out</button>
        </div>
      </aside>

      <main style={s.main}>
        <Outlet />
      </main>
    </div>
  );
}
