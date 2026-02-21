import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { campaignAPI } from '../services/api';

const scoreColor = (s) => s >= 0.7 ? 'var(--green)' : s >= 0.4 ? 'var(--yellow)' : 'var(--red)';
const statusColor = { active:'var(--green)', paused:'var(--yellow)', stopped:'var(--red)', draft:'var(--accent4)', completed:'var(--accent)' };
const fmtMoney = (n) => `₨${(n||0).toLocaleString('en-PK')}`;
const filters = ['all', 'active', 'paused', 'stopped', 'draft', 'completed'];

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
    setDeleting(id);
    try {
      await campaignAPI.delete(id);
      showToast('✓ Campaign deleted', 'success');
      load();
    } catch { showToast('⚠ Delete failed', 'error'); }
    setDeleting(null);
  };

  const showToast = (msg, type) => {
    setToast({ msg, type });
    setTimeout(() => setToast(null), 3000);
  };

  return (
    <div style={{ padding:'32px 36px', maxWidth:1200 }}>
      {/* Toast */}
      {toast && (
        <div style={{
          position:'fixed', top:24, right:24, zIndex:1000,
          background: toast.type==='success' ? 'linear-gradient(90deg, var(--accent5), var(--accent6))' : 'linear-gradient(90deg, var(--red), var(--accent3))',
          color: '#fff',
          fontWeight:700, fontSize:15, padding:'16px 26px', borderRadius:14, boxShadow:'0 2px 12px 0 rgba(0,0,0,0.12)',
        }}>{toast.msg}</div>
      )}

      <div style={{ display:'flex', alignItems:'center', justifyContent:'space-between', marginBottom:28 }}>
        <button
          onClick={() => navigate('/campaigns/new')}
          className="vivid-btn"
          style={{ padding:'12px 28px', fontSize:15 }}
        >
          + New Campaign
        </button>
      </div>

      {/* Filter tabs */}
      <div style={{ display:'flex', gap:8, marginBottom:28, background:'linear-gradient(90deg, var(--accent2), var(--accent3))', padding:8, borderRadius:12, border:'none', width:'fit-content', boxShadow:'0 2px 8px 0 var(--accent2)22' }}>
        {filters.map(f => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={filter===f ? 'vivid-btn' : ''}
            style={{
              padding:'10px 22px', borderRadius:10, border:'none', fontSize:15, fontWeight:700,
              background: filter===f ? undefined : 'transparent',
              color: filter===f ? '#fff' : 'var(--accent4)',
              boxShadow: filter===f ? '0 2px 8px 0 var(--accent2)33' : 'none',
              transition:'all .15s',
            }}
          >
            {f.charAt(0).toUpperCase()+f.slice(1)}
          </button>
        ))}
      </div>

      {loading ? (
        <div style={{ textAlign:'center', color:'var(--accent4)', fontFamily:'var(--font-mono)', letterSpacing:2, padding:60, fontSize:22 }}>LOADING...</div>
      ) : campaigns.length === 0 ? (
        <div style={{ textAlign:'center', padding:80, color:'var(--accent4)' }}>
          <div style={{ fontSize:54, marginBottom:18, color:'var(--accent2)' }}>◈</div>
          <p style={{ fontSize:18, marginBottom:10, fontWeight:700 }}>No campaigns found</p>
          <p style={{ fontSize:15 }}>
            {filter !== 'all' ? `No ${filter} campaigns.` : 'Create your first campaign to get started.'}
          </p>
          {filter === 'all' && (
            <button
              onClick={() => navigate('/campaigns/new')}
              className="vivid-btn"
              style={{ marginTop:24, padding:'12px 32px', fontSize:16 }}
            >
              + Create Campaign
            </button>
          )}
        </div>
      ) : (
        <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fill,minmax(360px,1fr))', gap:22 }}>
          {campaigns.map(c => {
            const score = c.performance_score || 0.5;
            const pct = Math.min(100, ((c.spent_budget||0)/(c.total_budget||1))*100);
            // Vibrant card gradient
            const cardBg = `linear-gradient(135deg, var(--accent2) 0%, var(--accent3) 100%)`;
            return (
              <div key={c.id} style={{
                background: cardBg,
                border: 'none',
                borderRadius: 18,
                padding: 28, display:'flex', flexDirection:'column', gap:18,
                boxShadow: '0 4px 24px 0 rgba(0,0,0,0.12)',
                color: '#fff',
                transition:'border-color .2s',
              }}
                onMouseEnter={e=>e.currentTarget.style.boxShadow='0 8px 32px 0 var(--accent3)44'}
                onMouseLeave={e=>e.currentTarget.style.boxShadow='0 4px 24px 0 rgba(0,0,0,0.12)'}
              >
                {/* Card header */}
                <div style={{ display:'flex', justifyContent:'space-between', alignItems:'flex-start' }}>
                  <div>
                    <h3 style={{ fontSize:18, fontWeight:900, color:'#fff', marginBottom:6, letterSpacing:0.2 }}>{c.name}</h3>
                    <p style={{ fontSize:13, color:'var(--accent4)', fontWeight:700 }}>{c.objective || 'General'}</p>
                  </div>
                  <span className="vivid-status">{c.status}</span>
                </div>

                {/* Progress bar */}
                <div style={{ display:'flex', alignItems:'center', gap:10 }}>
                  <div style={{ flex:1, height:7, background:'var(--bg3)', borderRadius:4 }}>
                    <div style={{ width:`${pct}%`, height:'100%', borderRadius:4, background: pct>90?'var(--red)':pct>60?'var(--yellow)':'var(--accent)', transition:'width .3s', boxShadow:'0 2px 8px 0 var(--accent2)33' }} />
                  </div>
                  <span style={{ fontSize:13, fontFamily:'var(--font-mono)', color:scoreColor(score), minWidth:36, textAlign:'right', fontWeight:700 }}>{(score*100).toFixed(0)}%</span>
                </div>

                {/* Metrics row */}
                <div style={{ display:'grid', gridTemplateColumns:'repeat(3,1fr)', gap:10 }}>
                  {[
                    { label:'Impressions', val:(c.metrics?.impressions||c.impressions||0).toLocaleString() },
                    { label:'Clicks',      val:(c.metrics?.clicks||c.clicks||0).toLocaleString() },
                    { label:'Conversions', val:(c.metrics?.conversions||c.conversions||0).toLocaleString() },
                  ].map(m => (
                    <div key={m.label} style={{ fontSize:14, color:'#fff', fontFamily:'var(--font-mono)', fontWeight:700 }}>
                      <span style={{ color:'var(--accent6)' }}>{m.val}</span> {m.label}
                    </div>
                  ))}
                </div>

                {/* Budget row */}
                <div style={{ display:'flex', gap:14, marginTop:2, fontSize:14, fontFamily:'var(--font-mono)', fontWeight:700 }}>
                  <span style={{ color:'var(--accent4)' }}>₨{(c.total_budget||0).toLocaleString('en-PK')}</span>
                  <span style={{ color:'var(--accent5)' }}>₨{(c.spent_budget||0).toLocaleString('en-PK')} spent</span>
                </div>

                {/* Actions */}
                <div style={{ display:'flex', gap:10, marginTop:4 }}>
                  <button
                    onClick={() => optimize(c.id)}
                    disabled={optimizing===c.id}
                    className="vivid-btn"
                    style={{ flex:1, padding:'10px', fontSize:14 }}
                  >
                    {optimizing===c.id ? '...' : '⚡ OPTIMIZE'}
                  </button>
                  <button
                    onClick={() => deleteCampaign(c.id)}
                    disabled={deleting===c.id}
                    style={{
                      flex:1, padding:'10px', borderRadius:10, border:'none',
                      background:'linear-gradient(90deg, var(--red), var(--accent3))', color:'#fff', fontSize:14, fontWeight:700, boxShadow:'0 2px 8px 0 var(--red)22', transition:'all .2s',
                    }}
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
