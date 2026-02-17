import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { campaignAPI } from '../services/api';

const scoreColor = (s) => s >= 0.7 ? 'var(--green)' : s >= 0.4 ? 'var(--yellow)' : 'var(--red)';
const statusColor = { active:'var(--green)', paused:'var(--yellow)', stopped:'var(--red)', draft:'var(--text3)', completed:'var(--accent)' };
const fmtMoney = (n) => `$${(n||0).toLocaleString()}`;

export default function Campaigns() {
  const navigate = useNavigate();
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading]     = useState(true);
  const [filter, setFilter]       = useState('all');
  const [optimizing, setOptimizing] = useState(null);
  const [toast, setToast]         = useState(null);
  const [deleting, setDeleting]   = useState(null);

  const load = async () => {
    setLoading(true);
    try {
      const res = await campaignAPI.list(filter === 'all' ? null : filter);
      setCampaigns(res.data.campaigns || []);
    } catch {}
    setLoading(false);
  };

  useEffect(() => { load(); }, [filter]);

  const optimize = async (id) => {
    setOptimizing(id);
    try {
      const res = await campaignAPI.optimize(id);
      const n = res.data.actions_taken?.length || 0;
      showToast(`✓ ${n} AI optimization action${n!==1?'s':''} taken`, 'success');
      load();
    } catch { showToast('⚠ Optimization failed', 'error'); }
    setOptimizing(null);
  };

  const deleteCampaign = async (id) => {
    if (!window.confirm('Delete this campaign?')) return;
    setDeleting(id);
    try {
      await campaignAPI.delete(id);
      showToast('Campaign deleted', 'success');
      load();
    } catch { showToast('Delete failed', 'error'); }
    setDeleting(null);
  };

  const showToast = (msg, type) => {
    setToast({ msg, type });
    setTimeout(() => setToast(null), 3500);
  };

  const filters = ['all','active','paused','stopped','completed'];

  return (
    <div style={{ padding:'32px 36px', maxWidth:1200 }}>

      {/* Toast */}
      {toast && (
        <div style={{
          position:'fixed', top:24, right:24, zIndex:999,
          padding:'12px 20px', borderRadius:10, fontSize:13, fontWeight:600,
          background: toast.type==='success' ? 'rgba(0,232,143,0.15)' : 'rgba(255,69,96,0.15)',
          border: `1px solid ${toast.type==='success' ? 'rgba(0,232,143,0.4)' : 'rgba(255,69,96,0.4)'}`,
          color: toast.type==='success' ? 'var(--green)' : 'var(--red)',
          boxShadow:'0 8px 32px rgba(0,0,0,0.4)',
        }}>
          {toast.msg}
        </div>
      )}

      {/* Header */}
      <div style={{ display:'flex', justifyContent:'space-between', alignItems:'flex-start', marginBottom:28 }}>
        <div>
          <h1 style={{ fontFamily:'var(--font-head)', fontSize:28, fontWeight:800, letterSpacing:'-1px' }}>Campaigns</h1>
          <p style={{ color:'var(--text3)', fontSize:13, marginTop:4 }}>{campaigns.length} campaign{campaigns.length!==1?'s':''} found</p>
        </div>
        <button
          onClick={() => navigate('/campaigns/new')}
          style={{ padding:'10px 20px', background:'linear-gradient(135deg,var(--accent2),var(--accent))', border:'none', borderRadius:10, color:'#fff', fontSize:13, fontWeight:700 }}
        >
          + New Campaign
        </button>
      </div>

      {/* Filter tabs */}
      <div style={{ display:'flex', gap:6, marginBottom:24, background:'var(--bg2)', padding:6, borderRadius:10, border:'1px solid var(--border)', width:'fit-content' }}>
        {filters.map(f => (
          <button key={f} onClick={() => setFilter(f)} style={{
            padding:'6px 16px', borderRadius:7, border:'none', fontSize:12,
            fontFamily:'var(--font-mono)', textTransform:'uppercase', letterSpacing:1,
            background: filter===f ? 'var(--bg3)' : 'transparent',
            color: filter===f ? 'var(--text)' : 'var(--text3)',
            fontWeight: filter===f ? 600 : 400,
            boxShadow: filter===f ? '0 1px 4px rgba(0,0,0,0.3)' : 'none',
            transition:'all .15s',
          }}>{f}</button>
        ))}
      </div>

      {/* Campaigns grid */}
      {loading ? (
        <div style={{ textAlign:'center', color:'var(--text3)', fontFamily:'var(--font-mono)', letterSpacing:2, padding:60 }}>LOADING...</div>
      ) : campaigns.length === 0 ? (
        <div style={{ textAlign:'center', padding:80, color:'var(--text3)' }}>
          <div style={{ fontSize:48, marginBottom:16 }}>◈</div>
          <p style={{ fontSize:16, marginBottom:8 }}>No campaigns found</p>
          <p style={{ fontSize:13 }}>
            {filter !== 'all' ? `No ${filter} campaigns.` : 'Create your first campaign to get started.'}
          </p>
          {filter === 'all' && (
            <button
              onClick={() => navigate('/campaigns/new')}
              style={{ marginTop:20, padding:'10px 24px', background:'var(--bg2)', border:'1px solid var(--border)', borderRadius:10, color:'var(--accent)', fontSize:13, fontWeight:600 }}
            >
              + Create Campaign
            </button>
          )}
        </div>
      ) : (
        <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fill,minmax(340px,1fr))', gap:16 }}>
          {campaigns.map(c => {
            const score = c.performance_score || 0.5;
            const pct = Math.min(100, ((c.spent_budget||0)/(c.total_budget||1))*100);
            return (
              <div key={c.id} style={{
                background:'var(--bg2)', border:'1px solid var(--border)', borderRadius:14,
                padding:22, display:'flex', flexDirection:'column', gap:14,
                transition:'border-color .2s',
              }}
                onMouseEnter={e=>e.currentTarget.style.borderColor='var(--accent)50'}
                onMouseLeave={e=>e.currentTarget.style.borderColor='var(--border)'}
              >
                {/* Card header */}
                <div style={{ display:'flex', justifyContent:'space-between', alignItems:'flex-start' }}>
                  <div>
                    <h3 style={{ fontSize:15, fontWeight:700, color:'var(--text)', marginBottom:4 }}>{c.name}</h3>
                    <p style={{ fontSize:12, color:'var(--text3)' }}>{c.objective || 'General'}</p>
                  </div>
                  <span style={{
                    fontSize:11, fontFamily:'var(--font-mono)', padding:'3px 10px', borderRadius:20,
                    background:`${statusColor[c.status]||'var(--text3)'}18`,
                    color:statusColor[c.status]||'var(--text3)',
                  }}>{c.status}</span>
                </div>

                {/* Budget bar */}
                <div>
                  <div style={{ display:'flex', justifyContent:'space-between', fontSize:12, marginBottom:6 }}>
                    <span style={{ color:'var(--text3)', fontFamily:'var(--font-mono)' }}>Budget used</span>
                    <span style={{ color:'var(--text)', fontFamily:'var(--font-mono)' }}>{fmtMoney(c.spent_budget)} / {fmtMoney(c.total_budget)}</span>
                  </div>
                  <div style={{ height:5, background:'var(--bg3)', borderRadius:3 }}>
                    <div style={{ width:`${pct}%`, height:'100%', borderRadius:3, background: pct>90?'var(--red)':pct>60?'var(--yellow)':'var(--accent)', transition:'width .3s' }} />
                  </div>
                </div>

                {/* Metrics row */}
                <div style={{ display:'grid', gridTemplateColumns:'repeat(3,1fr)', gap:8 }}>
                  {[
                    { label:'Impressions', val:(c.metrics?.impressions||c.impressions||0).toLocaleString() },
                    { label:'Clicks',      val:(c.metrics?.clicks||c.clicks||0).toLocaleString() },
                    { label:'Conversions', val:(c.metrics?.conversions||c.conversions||0).toLocaleString() },
                  ].map(m => (
                    <div key={m.label} style={{ background:'var(--bg3)', borderRadius:8, padding:'8px 10px', textAlign:'center' }}>
                      <div style={{ fontSize:15, fontWeight:700, fontFamily:'var(--font-head)', color:'var(--text)' }}>{m.val}</div>
                      <div style={{ fontSize:10, color:'var(--text3)', fontFamily:'var(--font-mono)', letterSpacing:0.5, marginTop:2 }}>{m.label}</div>
                    </div>
                  ))}
                </div>

                {/* AI Score */}
                <div style={{ display:'flex', alignItems:'center', gap:10 }}>
                  <span style={{ fontSize:11, fontFamily:'var(--font-mono)', color:'var(--text3)', letterSpacing:1 }}>AI SCORE</span>
                  <div style={{ flex:1, height:4, background:'var(--bg3)', borderRadius:2 }}>
                    <div style={{ width:`${score*100}%`, height:'100%', borderRadius:2, background:scoreColor(score) }} />
                  </div>
                  <span style={{ fontSize:12, fontFamily:'var(--font-mono)', color:scoreColor(score), minWidth:32, textAlign:'right' }}>{(score*100).toFixed(0)}%</span>
                </div>

                {/* Actions */}
                <div style={{ display:'flex', gap:8, marginTop:2 }}>
                  <button
                    onClick={() => optimize(c.id)}
                    disabled={optimizing===c.id}
                    style={{
                      flex:1, padding:'8px', borderRadius:8, border:'1px solid var(--accent)',
                      background:'rgba(0,212,255,0.08)', color:'var(--accent)',
                      fontSize:12, fontFamily:'var(--font-mono)', fontWeight:600,
                      transition:'all .2s',
                    }}
                  >
                    {optimizing===c.id ? '...' : '⚡ OPTIMIZE'}
                  </button>
                  <button
                    onClick={() => deleteCampaign(c.id)}
                    disabled={deleting===c.id}
                    style={{
                      padding:'8px 12px', borderRadius:8, border:'1px solid var(--border)',
                      background:'transparent', color:'var(--text3)', fontSize:12, transition:'all .2s',
                    }}
                    onMouseEnter={e=>{ e.target.style.borderColor='var(--red)'; e.target.style.color='var(--red)'; }}
                    onMouseLeave={e=>{ e.target.style.borderColor='var(--border)'; e.target.style.color='var(--text3)'; }}
                  >
                    {deleting===c.id ? '...' : '✕'}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
