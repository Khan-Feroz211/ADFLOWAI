import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI } from '../services/api';

const s = {
  page: {
    minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center',
    background: 'var(--bg)',
    backgroundImage: `
      radial-gradient(ellipse 80% 50% at 20% 40%, rgba(0,212,255,0.06) 0%, transparent 60%),
      radial-gradient(ellipse 60% 40% at 80% 60%, rgba(124,58,237,0.06) 0%, transparent 60%)
    `,
  },
  card: {
    width: 400, padding: 48,
    background: 'var(--bg2)',
    border: '1px solid var(--border)',
    borderRadius: 20,
  },
  logo: {
    fontFamily: 'var(--font-head)', fontSize: 28, fontWeight: 800,
    color: 'var(--accent)', marginBottom: 4, letterSpacing: '-1px',
  },
  tagline: { fontSize: 13, color: 'var(--text3)', fontFamily: 'var(--font-mono)', letterSpacing: 1, marginBottom: 40 },
  tabs: { display: 'flex', gap: 0, marginBottom: 32, background: 'var(--bg3)', borderRadius: 8, padding: 4 },
  tab: (active) => ({
    flex: 1, padding: '8px 0', border: 'none', borderRadius: 6, fontSize: 13, fontWeight: 600,
    background: active ? 'var(--bg2)' : 'transparent',
    color: active ? 'var(--text)' : 'var(--text3)',
    boxShadow: active ? '0 1px 4px rgba(0,0,0,0.3)' : 'none',
    transition: 'all .2s',
  }),
  label: { fontSize: 12, fontFamily: 'var(--font-mono)', color: 'var(--text3)', letterSpacing: 1, marginBottom: 6, display: 'block', textTransform: 'uppercase' },
  input: {
    width: '100%', padding: '12px 14px', marginBottom: 16,
    background: 'var(--bg3)', border: '1px solid var(--border)',
    borderRadius: 8, color: 'var(--text)', fontSize: 14, outline: 'none',
    transition: 'border-color .2s',
  },
  btn: {
    width: '100%', padding: '13px', marginTop: 8,
    background: 'linear-gradient(135deg, var(--accent2), var(--accent))',
    border: 'none', borderRadius: 8, color: '#fff',
    fontSize: 14, fontWeight: 700, letterSpacing: 0.5,
    transition: 'opacity .2s',
  },
  error: { background: 'rgba(255,69,96,0.1)', border: '1px solid rgba(255,69,96,0.3)', borderRadius: 8, padding: '10px 14px', fontSize: 13, color: 'var(--red)', marginBottom: 16 },
  success: { background: 'rgba(0,232,143,0.1)', border: '1px solid rgba(0,232,143,0.3)', borderRadius: 8, padding: '10px 14px', fontSize: 13, color: 'var(--green)', marginBottom: 16 },
};

function LoginInput({ label, type = 'text', placeholder, value, onChange }) {
  return (
    <div>
      <label style={s.label}>{label}</label>
      <input
        style={s.input}
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        onFocus={e => e.target.style.borderColor = 'var(--accent)'}
        onBlur={e => e.target.style.borderColor = 'var(--border)'}
      />
    </div>
  );
}

export default function Login() {
  const navigate = useNavigate();
  const [tab, setTab] = useState('login');
  const [form, setForm] = useState({ username: '', email: '', password: '', full_name: '', company: '' });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const set = (k) => (e) => setForm(f => ({ ...f, [k]: e.target.value }));

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await authAPI.login({ username: form.username, password: form.password });
      localStorage.setItem('access_token', res.data.tokens.access_token);
      localStorage.setItem('refresh_token', res.data.tokens.refresh_token);
      localStorage.setItem('user', JSON.stringify(res.data.user));
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.error || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await authAPI.register(form);
      localStorage.setItem('access_token', res.data.tokens.access_token);
      localStorage.setItem('refresh_token', res.data.tokens.refresh_token);
      localStorage.setItem('user', JSON.stringify(res.data.user));
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.error || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={s.page}>
      <div style={s.card}>
        <div style={s.logo}>ADFLOW<span style={{ color: 'var(--text2)' }}>AI</span></div>
        <div style={s.tagline}>AI-POWERED CAMPAIGN OPTIMIZER</div>

        <div style={s.tabs}>
          <button style={s.tab(tab === 'login')} onClick={() => { setTab('login'); setError(''); }}>Sign In</button>
          <button style={s.tab(tab === 'register')} onClick={() => { setTab('register'); setError(''); }}>Register</button>
        </div>

        {error && <div style={s.error}>! {error}</div>}
        {success && <div style={s.success}>OK {success}</div>}

        {tab === 'login' ? (
          <form onSubmit={handleLogin}>
            <LoginInput label="Username or Email" value={form.username} onChange={set('username')} placeholder="your username" />
            <LoginInput label="Password" value={form.password} onChange={set('password')} type="password" placeholder="********" />
            <button style={s.btn} type="submit" disabled={loading}>
              {loading ? 'Signing in...' : 'Sign In ->'}
            </button>
          </form>
        ) : (
          <form onSubmit={handleRegister}>
            <LoginInput label="Username" value={form.username} onChange={set('username')} placeholder="john_doe" />
            <LoginInput label="Email" value={form.email} onChange={set('email')} type="email" placeholder="john@company.com" />
            <LoginInput label="Password" value={form.password} onChange={set('password')} type="password" placeholder="Min 8 chars, uppercase + number" />
            <LoginInput label="Full Name (optional)" value={form.full_name} onChange={set('full_name')} placeholder="John Doe" />
            <LoginInput label="Company (optional)" value={form.company} onChange={set('company')} placeholder="Acme Inc." />
            <button style={s.btn} type="submit" disabled={loading}>
              {loading ? 'Creating account...' : 'Create Account ->'}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
