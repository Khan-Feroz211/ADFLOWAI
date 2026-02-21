import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI } from '../services/api';

const s = {
  page: {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: 'var(--bg)',
    backgroundImage: `
      radial-gradient(ellipse 80% 50% at 20% 40%, rgba(0,212,255,0.06) 0%, transparent 60%),
      radial-gradient(ellipse 60% 40% at 80% 60%, rgba(124,58,237,0.06) 0%, transparent 60%)
    `,
  },
  card: {
    width: 400,
    padding: 48,
    background: 'var(--bg2)',
    border: '1px solid var(--border)',
    borderRadius: 20,
  },
  logo: {
    fontFamily: 'var(--font-head)',
    fontSize: 28,
    fontWeight: 800,
    color: 'var(--accent)',
    marginBottom: 4,
    letterSpacing: '-1px',
  },
  tagline: {
    fontSize: 13,
    color: 'var(--text3)',
    fontFamily: 'var(--font-mono)',
    letterSpacing: 1,
    marginBottom: 40,
  },
  tabs: { display: 'flex', gap: 0, marginBottom: 32, background: 'var(--bg3)', borderRadius: 8, padding: 4 },
  tab: (active) => ({
    flex: 1,
    padding: '8px 0',
    border: 'none',
    borderRadius: 6,
    fontSize: 13,
    fontWeight: 600,
    background: active ? 'var(--bg2)' : 'transparent',
    color: active ? 'var(--text)' : 'var(--text3)',
    boxShadow: active ? '0 1px 4px rgba(0,0,0,0.3)' : 'none',
    transition: 'all .2s',
  }),
  label: {
    fontSize: 12,
    fontFamily: 'var(--font-mono)',
    color: 'var(--text3)',
    letterSpacing: 1,
    marginBottom: 6,
    display: 'block',
    textTransform: 'uppercase',
  },
  input: {
    width: '100%',
    padding: '12px 14px',
    marginBottom: 16,
    background: 'var(--bg3)',
    border: '1px solid var(--border)',
    borderRadius: 8,
    color: 'var(--text)',
    fontSize: 14,
    outline: 'none',
    transition: 'border-color .2s',
  },
  btn: {
    width: '100%',
    padding: '13px',
    marginTop: 8,
    background: 'linear-gradient(135deg, var(--accent2), var(--accent))',
    border: 'none',
    borderRadius: 8,
    color: '#fff',
    fontSize: 14,
    fontWeight: 700,
    letterSpacing: 0.5,
    transition: 'opacity .2s',
  },
  error: {
    background: 'rgba(255,69,96,0.1)',
    border: '1px solid rgba(255,69,96,0.3)',
    borderRadius: 8,
    padding: '10px 14px',
    fontSize: 13,
    color: 'var(--red)',
    marginBottom: 16,
  },
  success: {
    background: 'rgba(0,232,143,0.1)',
    border: '1px solid rgba(0,232,143,0.3)',
    borderRadius: 8,
    padding: '10px 14px',
    fontSize: 13,
    color: 'var(--green)',
    marginBottom: 16,
  },
};

// Small presentational Input moved to top-level to avoid remounting on each render
function Input({ label, name, type = 'text', placeholder, value, onChange, onFocus, onBlur }) {
  return (
    <div>
      <label style={s.label}>{label}</label>
      <input
        style={s.input}
        type={type}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        onFocus={onFocus}
        onBlur={onBlur}
      />
    </div>
  );
}

export default function Login() {
  const navigate = useNavigate();
  const [tab, setTab] = useState('login');
  const [form, setForm] = useState({ username: '', email: '', password: '', full_name: '', company: '' });
  const [errors, setErrors] = useState([]);
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }));

  const handleLogin = async (e) => {
    e.preventDefault();
    const validationErrors = [];
    if (!form.username.trim()) validationErrors.push('Username or email is required');
    if (!form.password) validationErrors.push('Password is required');
    if (validationErrors.length > 0) {
      setErrors(validationErrors);
      return;
    }

    setErrors([]);
    setLoading(true);
    try {
      const res = await authAPI.login({ username: form.username, password: form.password });
      localStorage.setItem('access_token', res.data.tokens.access_token);
      localStorage.setItem('refresh_token', res.data.tokens.refresh_token);
      localStorage.setItem('user', JSON.stringify(res.data.user));
      navigate('/');
    } catch (err) {
      const apiErrors = err.response?.data?.errors;
      if (Array.isArray(apiErrors) && apiErrors.length > 0) setErrors(apiErrors);
      else setErrors([err.response?.data?.error || 'Login failed']);
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    const validationErrors = [];
    if (!form.username.trim()) validationErrors.push('Username is required');
    if (!form.email.trim()) validationErrors.push('Email is required');
    if (form.email && !form.email.includes('@')) validationErrors.push('Email format looks invalid');
    if (!form.password) validationErrors.push('Password is required');
    if (form.password && form.password.length < 8) validationErrors.push('Password must be at least 8 characters');
    if (validationErrors.length > 0) {
      setErrors(validationErrors);
      return;
    }

    setErrors([]);
    setLoading(true);
    try {
      const res = await authAPI.register(form);
      localStorage.setItem('access_token', res.data.tokens.access_token);
      localStorage.setItem('refresh_token', res.data.tokens.refresh_token);
      localStorage.setItem('user', JSON.stringify(res.data.user));
      navigate('/');
    } catch (err) {
      const apiErrors = err.response?.data?.errors;
      if (Array.isArray(apiErrors) && apiErrors.length > 0) setErrors(apiErrors);
      else setErrors([err.response?.data?.error || 'Registration failed']);
    } finally {
      setLoading(false);
    }
  };

  const inputFocus = (e) => (e.target.style.borderColor = 'var(--accent)');
  const inputBlur = (e) => (e.target.style.borderColor = 'var(--border)');

  return (
    <div style={s.page}>
      <div style={s.card}>
        <div style={s.logo}>
          ADFLOW<span style={{ color: 'var(--text2)' }}>AI</span>
        </div>
        <div style={s.tagline}>AI-POWERED CAMPAIGN OPTIMIZER</div>

        <div style={s.tabs}>
          <button style={s.tab(tab === 'login')} onClick={() => { setTab('login'); setErrors([]); }}>
            Sign In
          </button>
          <button style={s.tab(tab === 'register')} onClick={() => { setTab('register'); setErrors([]); }}>
            Register
          </button>
        </div>

        {errors.length > 0 && (
          <div style={s.error}>
            {errors.map((msg, idx) => (
              <div key={`${idx}-${msg}`}>! {msg}</div>
            ))}
          </div>
        )}
        {success && <div style={s.success}>OK {success}</div>}

        {tab === 'login' ? (
          <form onSubmit={handleLogin}>
            <Input label="Username or Email" name="username" placeholder="your username"
              value={form.username} onChange={set('username')} onFocus={inputFocus} onBlur={inputBlur} />
            <Input label="Password" name="password" type="password" placeholder="********"
              value={form.password} onChange={set('password')} onFocus={inputFocus} onBlur={inputBlur} />
            <button style={s.btn} type="submit" disabled={loading}>
              {loading ? 'Signing in...' : 'Sign In ->'}
            </button>
          </form>
        ) : (
          <form onSubmit={handleRegister}>
            <Input label="Username" name="username" placeholder="john_doe"
              value={form.username} onChange={set('username')} onFocus={inputFocus} onBlur={inputBlur} />
            <Input label="Email" name="email" type="email" placeholder="john@company.com"
              value={form.email} onChange={set('email')} onFocus={inputFocus} onBlur={inputBlur} />
            <Input label="Password" name="password" type="password" placeholder="Min 8 chars, uppercase + number"
              value={form.password} onChange={set('password')} onFocus={inputFocus} onBlur={inputBlur} />
            <Input label="Full Name (optional)" name="full_name" placeholder="John Doe"
              value={form.full_name} onChange={set('full_name')} onFocus={inputFocus} onBlur={inputBlur} />
            <Input label="Company (optional)" name="company" placeholder="Acme Inc."
              value={form.company} onChange={set('company')} onFocus={inputFocus} onBlur={inputBlur} />
            <button style={s.btn} type="submit" disabled={loading}>
              {loading ? 'Creating account...' : 'Create Account ->'}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
