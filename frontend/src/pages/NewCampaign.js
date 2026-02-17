import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { campaignAPI } from '../services/api';

const platforms = [
  { id:'google_ads', name:'Google Ads',   icon:'G', color:'#4285f4' },
  { id:'facebook',   name:'Facebook Ads', icon:'f', color:'#1877f2' },
  { id:'instagram',  name:'Instagram',    icon:'◈', color:'#e1306c' },
  { id:'linkedin',   name:'LinkedIn Ads', icon:'in', color:'#0a66c2' },
  { id:'twitter',    name:'Twitter Ads',  icon:'✕', color:'#1da1f2' },
  { id:'tiktok',     name:'TikTok Ads',   icon:'♪', color:'#ff0050' },
];

const objectives = ['conversions','traffic','awareness','leads','engagement','sales'];

const s = {
  page:  { padding:'32px 36px', maxWidth:760 },
  back:  { fontSize:13, color:'var(--text3)', background:'none', border:'none', cursor:'pointer', padding:0, marginBottom:24, display:'flex', alignItems:'center', gap:6 },
  card:  { background:'var(--bg2)', border:'1px solid var(--border)', borderRadius:14, padding:28, marginBottom:20 },
  sectionTitle: { fontFamily:'var(--font-mono)', fontSize:11, letterSpacing:2, color:'var(--text3)', textTransform:'uppercase', marginBottom:18 },
  label: { fontSize:12, fontFamily:'var(--font-mono)', color:'var(--text3)', letterSpacing:1, textTransform:'uppercase', marginBottom:6, display:'block' },
  input: {
    width:'100%', padding:'11px 14px', background:'var(--bg3)',
    border:'1px solid var(--border)', borderRadius:8,
    color:'var(--text)', fontSize:14, outline:'none', transition:'border-color .2s',
  },
  row:   { display:'grid', gridTemplateColumns:'1fr 1fr', gap:16, marginBottom:16 },
  platformGrid: { display:'grid', gridTemplateColumns:'repeat(3,1fr)', gap:10 },
  platformBtn: (selected, color) => ({
    padding:'12px 10px', borderRadius:10, border:`1px solid ${selected ? color : 'var(--border)'}`,
    background: selected ? `${color}18` : 'var(--bg3)',
    color: selected ? color : 'var(--text2)',
    fontSize:13, fontWeight:600, cursor:'pointer', transition:'all .2s',
    display:'flex', flexDirection:'column', alignItems:'center', gap:6,
  }),
  platformIcon: (color) => ({
    width:28, height:28, borderRadius:8, background:color,
    display:'flex', alignItems:'center', justifyContent:'center',
    fontSize:12, fontWeight:900, color:'#fff',
  }),
  objGrid: { display:'grid', gridTemplateColumns:'repeat(3,1fr)', gap:8 },
  objBtn: (sel) => ({
    padding:'10px', borderRadius:8,
    border:`1px solid ${sel?'var(--accent)':'var(--border)'}`,
    background: sel?'rgba(0,212,255,0.1)':'var(--bg3)',
    color: sel?'var(--accent)':'var(--text2)',
    fontSize:13, fontWeight:500, cursor:'pointer', transition:'all .2s',
    textTransform:'capitalize',
  }),
  submitBtn: {
    width:'100%', padding:'14px', marginTop:8,
    background:'linear-gradient(135deg,var(--accent2),var(--accent))',
    border:'none', borderRadius:10, color:'#fff',
    fontSize:15, fontWeight:700, letterSpacing:0.5,
  },
  error: { background:'rgba(255,69,96,0.1)', border:'1px solid rgba(255,69,96,0.3)', borderRadius:8, padding:'10px 14px', fontSize:13, color:'var(--red)', marginBottom:16 },
};

export default function NewCampaign() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState('');
  const [form, setForm] = useState({
    name:'', total_budget:'', objective:'conversions',
    start_date:'', end_date:'', description:'',
    platforms:[],
    target_audience:{ locations:'', age_range:'18-45', interests:'' },
  });

  const set = (k) => (e) => setForm(f => ({ ...f, [k]: e.target.value }));
  const setAud = (k) => (e) => setForm(f => ({ ...f, target_audience:{ ...f.target_audience, [k]:e.target.value } }));

  const togglePlatform = (id) => setForm(f => ({
    ...f,
    platforms: f.platforms.includes(id)
      ? f.platforms.filter(p=>p!==id)
      : [...f.platforms, id],
  }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!form.name.trim())         return setError('Campaign name is required');
    if (!form.total_budget)        return setError('Budget is required');
    if (form.platforms.length===0) return setError('Select at least one platform');
    if (!form.start_date)          return setError('Start date is required');

    setLoading(true);
    try {
      const payload = {
        name:         form.name.trim(),
        total_budget: parseFloat(form.total_budget),
        objective:    form.objective,
        platforms:    form.platforms,
        start_date:   new Date(form.start_date).toISOString(),
        end_date:     form.end_date ? new Date(form.end_date).toISOString() : null,
        description:  form.description,
        target_audience: {
          locations: form.target_audience.locations.split(',').map(s=>s.trim()).filter(Boolean),
          age_range: form.target_audience.age_range,
          interests: form.target_audience.interests.split(',').map(s=>s.trim()).filter(Boolean),
        },
      };
      await campaignAPI.create(payload);
      navigate('/campaigns');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create campaign');
    }
    setLoading(false);
  };

  const focusBorder = (e) => e.target.style.borderColor = 'var(--accent)';
  const blurBorder  = (e) => e.target.style.borderColor = 'var(--border)';

  const Field = ({ label, name, type='text', placeholder, required }) => (
    <div style={{ marginBottom:16 }}>
      <label style={s.label}>{label}{required && ' *'}</label>
      <input
        style={s.input} type={type} value={form[name]}
        onChange={set(name)} placeholder={placeholder}
        onFocus={focusBorder} onBlur={blurBorder}
        required={required}
      />
    </div>
  );

  return (
    <div style={s.page}>

      <button style={s.back} onClick={() => navigate(-1)}>
        ← Back
      </button>

      <h1 style={{ fontFamily:'var(--font-head)', fontSize:28, fontWeight:800, letterSpacing:'-1px', marginBottom:8 }}>
        New Campaign
      </h1>
      <p style={{ color:'var(--text3)', fontSize:13, marginBottom:28 }}>
        Fill in the details — AI will optimize automatically once live.
      </p>

      {error && <div style={s.error}>⚠ {error}</div>}

      <form onSubmit={handleSubmit}>

        {/* ── Basic Info ─────────────────────────────── */}
        <div style={s.card}>
          <div style={s.sectionTitle}>01 — Basic Info</div>
          <Field label="Campaign Name" name="name" placeholder="e.g. Summer Sale 2026" required />
          <Field label="Description"   name="description" placeholder="What is this campaign about?" />

          <div style={s.row}>
            <div>
              <label style={s.label}>Objective *</label>
              <div style={s.objGrid}>
                {objectives.map(obj => (
                  <button key={obj} type="button" style={s.objBtn(form.objective===obj)} onClick={() => setForm(f=>({...f,objective:obj}))}>
                    {obj}
                  </button>
                ))}
              </div>
            </div>
            <div>
              <label style={s.label}>Total Budget (USD) *</label>
              <input
                style={{ ...s.input, fontSize:20, fontWeight:700, fontFamily:'var(--font-head)' }}
                type="number" min="1" step="any"
                value={form.total_budget} onChange={set('total_budget')}
                placeholder="5000"
                onFocus={focusBorder} onBlur={blurBorder}
              />
              {form.total_budget && (
                <p style={{ fontSize:11, color:'var(--text3)', marginTop:6, fontFamily:'var(--font-mono)' }}>
                  ${parseFloat(form.total_budget||0).toLocaleString()} total budget
                </p>
              )}
            </div>
          </div>
        </div>

        {/* ── Platforms ──────────────────────────────── */}
        <div style={s.card}>
          <div style={s.sectionTitle}>02 — Platforms * (select one or more)</div>
          <div style={s.platformGrid}>
            {platforms.map(p => (
              <button
                key={p.id} type="button"
                style={s.platformBtn(form.platforms.includes(p.id), p.color)}
                onClick={() => togglePlatform(p.id)}
              >
                <div style={s.platformIcon(p.color)}>{p.icon}</div>
                <span style={{ fontSize:11 }}>{p.name}</span>
                {form.platforms.includes(p.id) && (
                  <span style={{ fontSize:10, fontFamily:'var(--font-mono)', color:p.color }}>✓ selected</span>
                )}
              </button>
            ))}
          </div>
          {form.platforms.length > 0 && form.total_budget && (
            <div style={{ marginTop:16, padding:'10px 14px', background:'var(--bg3)', borderRadius:8 }}>
              <span style={{ fontSize:11, fontFamily:'var(--font-mono)', color:'var(--text3)', letterSpacing:1 }}>BUDGET SPLIT (AUTO) — </span>
              {form.platforms.map(pid => {
                const pl = platforms.find(p=>p.id===pid);
                const share = (parseFloat(form.total_budget||0)/form.platforms.length).toFixed(0);
                return (
                  <span key={pid} style={{ fontSize:11, fontFamily:'var(--font-mono)', color:'var(--text2)', marginRight:12 }}>
                    {pl?.name}: <span style={{ color:'var(--accent)' }}>${parseInt(share).toLocaleString()}</span>
                  </span>
                );
              })}
            </div>
          )}
        </div>

        {/* ── Schedule ───────────────────────────────── */}
        <div style={s.card}>
          <div style={s.sectionTitle}>03 — Schedule</div>
          <div style={s.row}>
            <Field label="Start Date *" name="start_date" type="date" required />
            <Field label="End Date (optional)" name="end_date" type="date" />
          </div>
        </div>

        {/* ── Audience ───────────────────────────────── */}
        <div style={s.card}>
          <div style={s.sectionTitle}>04 — Target Audience</div>
          <div style={{ marginBottom:16 }}>
            <label style={s.label}>Locations (comma separated)</label>
            <input style={s.input} value={form.target_audience.locations}
              onChange={setAud('locations')} placeholder="US, UK, CA, AU"
              onFocus={focusBorder} onBlur={blurBorder} />
          </div>
          <div style={s.row}>
            <div>
              <label style={s.label}>Age Range</label>
              <input style={s.input} value={form.target_audience.age_range}
                onChange={setAud('age_range')} placeholder="18-45"
                onFocus={focusBorder} onBlur={blurBorder} />
            </div>
            <div>
              <label style={s.label}>Interests (comma separated)</label>
              <input style={s.input} value={form.target_audience.interests}
                onChange={setAud('interests')} placeholder="technology, fashion, sports"
                onFocus={focusBorder} onBlur={blurBorder} />
            </div>
          </div>
        </div>

        {/* ── Submit ─────────────────────────────────── */}
        <button type="submit" style={s.submitBtn} disabled={loading}>
          {loading ? 'Creating Campaign...' : '⚡ Create Campaign & Start AI Optimization'}
        </button>

        <p style={{ fontSize:11, color:'var(--text3)', textAlign:'center', marginTop:12, fontFamily:'var(--font-mono)' }}>
          AI will begin optimizing this campaign automatically after creation
        </p>

      </form>
    </div>
  );
}
