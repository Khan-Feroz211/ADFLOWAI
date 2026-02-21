import React, { useState, useCallback } from 'react';
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

// Localized campaign types for Pakistan
const objectives = [
  { key: 'conversions', en: 'Conversions', ur: 'تبدیلیاں' },
  { key: 'traffic', en: 'Website Traffic', ur: 'ویب سائٹ ٹریفک' },
  { key: 'awareness', en: 'Brand Awareness', ur: 'برانڈ آگاہی' },
  { key: 'leads', en: 'Leads', ur: 'لیڈز' },
  { key: 'engagement', en: 'Engagement', ur: 'مشغولیت' },
  { key: 'sales', en: 'Sales', ur: 'فروخت' },
  { key: 'product_launch', en: 'Product Launch', ur: 'پروڈکٹ لانچ' },
  { key: 'event_promotion', en: 'Event Promotion', ur: 'ایونٹ پروموشن' },
  { key: 'political', en: 'Political', ur: 'سیاسی' },
  { key: 'religious', en: 'Religious', ur: 'مذہبی' },
  { key: 'ngo', en: 'NGO/Charity', ur: 'این جی او/چیریٹی' }
];

const FIELD_LIMITS = {
  name: 80,
  description: 300,
  locations: 120,
  age_range: 20,
  interests: 120
};

const s = {
  page:  { padding:'32px 36px', maxWidth:760 },
  back:  { fontSize:14, color:'var(--accent4)', background:'none', border:'none', cursor:'pointer', padding:0, marginBottom:28, display:'flex', alignItems:'center', gap:8, fontWeight:700 },
  card:  { background:'linear-gradient(135deg, var(--accent2) 0%, var(--accent3) 100%)', border:'none', borderRadius:18, padding:32, marginBottom:26, boxShadow:'0 4px 24px 0 rgba(0,0,0,0.12)', color:'#fff' },
  sectionTitle: { fontFamily:'var(--font-mono)', fontSize:13, letterSpacing:2, color:'#fff', textTransform:'uppercase', marginBottom:22, fontWeight:700, opacity:0.85 },
  label: { fontSize:13, fontFamily:'var(--font-mono)', color:'var(--accent4)', letterSpacing:1, textTransform:'uppercase', marginBottom:8, display:'block', fontWeight:700 },
  input: {
    width:'100%', padding:'13px 16px', background:'var(--bg3)',
    border:'1px solid var(--accent2)', borderRadius:10,
    color:'#fff', fontSize:15, outline:'none', transition:'border-color .2s', fontWeight:600,
  },
  row:   { display:'grid', gridTemplateColumns:'1fr 1fr', gap:18, marginBottom:18 },
  platformGrid: { display:'grid', gridTemplateColumns:'repeat(3,1fr)', gap:12 },
  platformBtn: (selected, color) => ({
    padding:'14px 12px', borderRadius:12, border:`2px solid ${selected ? color : 'var(--accent2)'}`,
    background: selected ? `linear-gradient(135deg, ${color} 0%, var(--accent2) 100%)` : 'var(--bg3)',
    color: selected ? '#fff' : 'var(--accent4)',
    fontSize:15, fontWeight:700, cursor:'pointer', transition:'all .2s',
    display:'flex', flexDirection:'column', alignItems:'center', gap:8,
    boxShadow: selected ? '0 2px 8px 0 '+color+'33' : 'none',
  }),
  platformIcon: (color) => ({
    width:32, height:32, borderRadius:10, background:color,
    display:'flex', alignItems:'center', justifyContent:'center',
    fontSize:15, fontWeight:900, color:'#fff',
    boxShadow:'0 2px 8px 0 '+color+'33',
  }),
  objGrid: { display:'grid', gridTemplateColumns:'repeat(3,1fr)', gap:10 },
  objBtn: (sel) => ({
    padding:'12px', borderRadius:10,
    border:`2px solid ${sel?'var(--accent3)':'var(--accent2)'}`,
    background: sel?'linear-gradient(90deg, var(--accent3), var(--accent4))':'var(--bg3)',
    color: sel?'#fff':'var(--accent4)',
    fontSize:15, fontWeight:700, cursor:'pointer', transition:'background .2s',
    textTransform:'capitalize',
    boxShadow: sel ? '0 2px 8px 0 var(--accent3)33' : 'none',
  }),
  submitBtn: {
    width:'100%', padding:'16px', marginTop:12,
    background:'linear-gradient(90deg, var(--accent2), var(--accent3))',
    border:'none', borderRadius:12, color:'#fff',
    fontSize:17, fontWeight:900, letterSpacing:0.5, boxShadow:'0 2px 8px 0 var(--accent2)33',
    transition:'background .2s, box-shadow .2s, transform .1s',
  },
  error: { background:'linear-gradient(90deg, var(--red), var(--accent3))', border:'none', borderRadius:10, padding:'12px 18px', fontSize:15, color:'#fff', marginBottom:18, fontWeight:700, boxShadow:'0 2px 8px 0 var(--red)22' },
};
// Top-level Field component avoids remounting/focus loss when parent rerenders
const Field = React.memo(function Field({ label, name, type='text', placeholder, required, value, onChange, maxLength }) {
  React.useEffect(() => {
    console.log('[Field] mount', name);
    return () => console.log('[Field] unmount', name);
  }, [name]);

  const _onChange = (e) => {
    console.log('[Field] change', name, e.target.value);
    onChange && onChange(e);
  };

  const _onKey = (e) => console.log('[Field] key', name, e.key);

  return (
    <div style={{ marginBottom:16 }}>
      <label style={s.label}>{label}{required && ' *'}</label>
      <input
        style={s.input}
        type={type}
        name={name}
        value={value ?? ''}
        onChange={_onChange}
        onKeyDown={_onKey}
        placeholder={placeholder}
        onFocus={(e) => e.target.style.borderColor = 'var(--accent)'}
        onBlur={(e) => e.target.style.borderColor = 'var(--border)'}
        required={required}
        maxLength={maxLength}
      />
      {maxLength && (
        <div style={{ fontSize:10, color:'var(--text3)', marginTop:2, textAlign:'right' }}>
          {(value?.length || 0)} / {maxLength} characters
        </div>
      )}
    </div>
  );
});

export default function NewCampaign() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [errors, setErrors]   = useState([]);
  const [form, setForm] = useState({
    name:'', total_budget:'', objective:'conversions',
    start_date:'', end_date:'', description:'',
    platforms:[],
    target_audience:{ locations:'', age_range:'18-45', interests:'' },
  });

  // Stable handlers for fields
  const setName = useCallback((e) => {
    const v = (e.target.value || '').slice(0, FIELD_LIMITS.name);
    setForm(f => ({ ...f, name: v }));
  }, []);
  const setDescription = useCallback((e) => {
    const v = (e.target.value || '').slice(0, FIELD_LIMITS.description);
    setForm(f => ({ ...f, description: v }));
  }, []);
  const setTotalBudget = useCallback((e) => {
    const v = e.target.value;
    setForm(f => ({ ...f, total_budget: v }));
  }, []);
  const setStartDate = useCallback((e) => setForm(f => ({ ...f, start_date: e.target.value })), []);
  const setEndDate = useCallback((e) => setForm(f => ({ ...f, end_date: e.target.value })), []);

  const setLocations = useCallback((e) => {
    const v = (e.target.value || '').slice(0, FIELD_LIMITS.locations);
    setForm(f => ({ ...f, target_audience: { ...f.target_audience, locations: v } }));
  }, []);
  const setAgeRange = useCallback((e) => {
    const v = (e.target.value || '').slice(0, FIELD_LIMITS.age_range);
    setForm(f => ({ ...f, target_audience: { ...f.target_audience, age_range: v } }));
  }, []);
  const setInterests = useCallback((e) => {
    const v = (e.target.value || '').slice(0, FIELD_LIMITS.interests);
    setForm(f => ({ ...f, target_audience: { ...f.target_audience, interests: v } }));
  }, []);

  const togglePlatform = (id) => setForm(f => ({
    ...f,
    platforms: f.platforms.includes(id)
      ? f.platforms.filter(p=>p!==id)
      : [...f.platforms, id],
  }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    const validationErrors = [];
    const parsedBudget = parseFloat(form.total_budget);

    if (!form.name.trim()) validationErrors.push('Campaign name is required');
    if (!form.total_budget || Number.isNaN(parsedBudget) || parsedBudget <= 0) {
      validationErrors.push('Budget must be a number greater than 0');
    }
    if (form.platforms.length === 0) validationErrors.push('Select at least one platform');
    if (!form.start_date) validationErrors.push('Start date is required');
    if (form.end_date && form.start_date && new Date(form.end_date) < new Date(form.start_date)) {
      validationErrors.push('End date must be on or after start date');
    }

    if (validationErrors.length > 0) {
      setErrors(validationErrors);
      return;
    }

    setLoading(true);
    try {
      const payload = {
        name:         form.name.trim(),
        total_budget: parsedBudget,
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
      const apiErrors = err.response?.data?.errors;
      if (Array.isArray(apiErrors) && apiErrors.length > 0) {
        setErrors(apiErrors);
      } else {
        setErrors([err.response?.data?.error || 'Failed to create campaign']);
      }
    }
    setLoading(false);
  };

  const focusBorder = (e) => e.target.style.borderColor = 'var(--accent)';
  const blurBorder  = (e) => e.target.style.borderColor = 'var(--border)';

  // Use top-level Field component; pass value, onChange and maxLength

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

      {errors.length > 0 && (
        <div style={s.error}>
          {errors.map((msg, idx) => (
            <div key={`${idx}-${msg}`}>⚠ {msg}</div>
          ))}
        </div>
      )}

      <form onSubmit={handleSubmit}>

        {/* ── Basic Info ─────────────────────────────── */}
        <div style={s.card}>
          <div style={s.sectionTitle}>01 — Basic Info / بنیادی معلومات</div>
          <Field label="Campaign Name / مہم کا نام" name="name" placeholder="e.g. Summer Sale 2026 / مثلاً سمر سیل 2026" required
            value={form.name} onChange={setName} maxLength={FIELD_LIMITS.name} />
          <Field label="Description / تفصیل" name="description" placeholder="What is this campaign about? / یہ مہم کس بارے میں ہے؟"
            value={form.description} onChange={setDescription} maxLength={FIELD_LIMITS.description} />

          <div style={s.row}>
            <div>
              <label style={s.label}>Objective / مقصد *</label>
              <div style={s.objGrid}>
                {objectives.map(obj => (
                  <button key={obj.key} type="button" style={s.objBtn(form.objective===obj.key)} onClick={() => setForm(f=>({...f,objective:obj.key}))}>
                    {obj.en} <span style={{fontSize:11, color:'var(--text3)', marginLeft:4}}>{obj.ur}</span>
                  </button>
                ))}
              </div>
            </div>
            <div>
              <label style={s.label}>Total Budget (PKR) *</label>
              <input
                style={{ ...s.input, fontSize:20, fontWeight:700, fontFamily:'var(--font-head)' }}
                type="number" min="1" step="any"
                value={form.total_budget ?? ''} onChange={setTotalBudget}
                placeholder="10000"
                onFocus={focusBorder} onBlur={blurBorder}
              />
              {form.total_budget && (
                <p style={{ fontSize:11, color:'var(--text3)', marginTop:6, fontFamily:'var(--font-mono)' }}>
                  ₨{parseFloat(form.total_budget||0).toLocaleString('en-PK')} total budget
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
                    {pl?.name}: <span style={{ color:'var(--accent)' }}>₨{parseInt(share).toLocaleString('en-PK')}</span>
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
            <Field label="Start Date *" name="start_date" type="date" required value={form.start_date} onChange={setStartDate} />
            <Field label="End Date (optional)" name="end_date" type="date" value={form.end_date} onChange={setEndDate} />
          </div>
        </div>

        {/* ── Audience ───────────────────────────────── */}
        <div style={s.card}>
          <div style={s.sectionTitle}>04 — Target Audience</div>
          <div style={{ marginBottom:16 }}>
            <label style={s.label}>Locations (comma separated)</label>
            <input style={s.input} value={form.target_audience.locations}
              onChange={setLocations} placeholder="Pakistan, Lahore, Karachi, Islamabad"
              onFocus={focusBorder} onBlur={blurBorder} maxLength={FIELD_LIMITS.locations} />
            <div style={{ fontSize:10, color:'var(--text3)', marginTop:2, textAlign:'right' }}>
              {form.target_audience.locations.length} / {FIELD_LIMITS.locations} characters
            </div>
          </div>
          <div style={s.row}>
            <div>
              <label style={s.label}>Age Range</label>
              <input style={s.input} value={form.target_audience.age_range}
                onChange={setAgeRange} placeholder="18-45"
                onFocus={focusBorder} onBlur={blurBorder} maxLength={FIELD_LIMITS.age_range} />
              <div style={{ fontSize:10, color:'var(--text3)', marginTop:2, textAlign:'right' }}>
                {form.target_audience.age_range.length} / {FIELD_LIMITS.age_range} characters
              </div>
            </div>
            <div>
              <label style={s.label}>Interests (comma separated)</label>
              <input style={s.input} value={form.target_audience.interests}
                onChange={setInterests} placeholder="technology, fashion, sports"
                onFocus={focusBorder} onBlur={blurBorder} maxLength={FIELD_LIMITS.interests} />
              <div style={{ fontSize:10, color:'var(--text3)', marginTop:2, textAlign:'right' }}>
                {form.target_audience.interests.length} / {FIELD_LIMITS.interests} characters
              </div>
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
