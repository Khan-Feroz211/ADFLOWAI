import React, { useState } from 'react';
import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import { authAPI } from '../services/api';

const s = {
  shell:   { display:'flex', height:'100vh', overflow:'hidden' },
  sidebar: {
    width: 240, minWidth: 240, background: 'var(--bg2)',
    borderRight: '1px solid var(--border)', display: 'flex',
    flexDirection: 'column', padding: '24px 0',
  },
  logo: {
    padding: '0 24px 32px', fontFamily: 'var(--font-head)',
    fontSize: 22, fontWeight: 800, letterSpacing: '-0.5px',
    color: 'var(--accent)',
  },
  logoSub: { fontSize: 10, color: 'var(--text3)', fontFamily: 'var(--font-mono)', letterSpacing: 2, display:'block', marginTop: 2 },
  nav:     { flex: 1, display: 'flex', flexDirection: 'column', gap: 4, padding: '0 12px' },
  link: (active) => ({
    display: 'flex', alignItems: 'center', gap: 12, padding: '10px 14px',
    borderRadius: 8, textDecoration: 'none', fontSize: 14, fontWeight: 500,
    color: active ? 'var(--text)' : 'var(--text2)',
    background: active ? 'var(--bg3)' : 'transparent',
    borderLeft: active ? '2px solid var(--accent)' : '2px solid transparent',
    transition: 'all .15s',
  }),
  section: { fontSize: 10, fontFamily: 'var(--font-mono)', color: 'var(--text3)', letterSpacing: 2, padding: '16px 26px 6px', textTransform: 'uppercase' },
  bottom:  { padding: '16px 12px', borderTop: '1px solid var(--border)', marginTop: 'auto' },
  user:    { display:'flex', alignItems:'center', gap: 10, padding: '8px 14px', borderRadius: 8 },
  avatar:  { width: 32, height: 32, borderRadius: '50%', background: 'linear-gradient(135deg,var(--accent2),var(--accent))', display:'flex', alignItems:'center', justifyContent:'center', fontSize: 13, fontWeight: 700, color:'#fff', flexShrink: 0 },
  userName:{ fontSize: 13, fontWeight: 600, color: 'var(--text)' },
  userRole:{ fontSize: 11, color: 'var(--text3)', fontFamily: 'var(--font-mono)' },
  logoutBtn:{ width:'100%', marginTop: 8, padding: '8px', background:'none', border:'1px solid var(--border)', borderRadius: 8, color:'var(--text2)', fontSize: 13, transition:'all .15s' },
  main:    { flex: 1, overflow: 'auto', background: 'var(--bg)' },
};

const navItems = [
  { to: '/',          icon: '▦', label: 'Dashboard' },
  { to: '/campaigns', icon: '◈', label: 'Campaigns' },
];

export default function Layout() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem('user') || '{}');

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
        <nav style={{ padding: '0 12px' }}>
          <NavLink to="/campaigns/new" style={({ isActive }) => s.link(isActive)}>
            <span style={{ fontSize: 16 }}>＋</span>
            New Campaign
          </NavLink>
        </nav>

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
