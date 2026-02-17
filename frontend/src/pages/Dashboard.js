import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { dashboardAPI, campaignAPI } from '../services/api';

// ── Helpers ──────────────────────────────────────────────────────────────────
const fmt = (n) => n >= 1000000 ? `${(n/1000000).toFixed(1)}M` : n >= 1000 ? `${(n/1000).toFixed(1)}K` : String(n||0);
const fmtMoney = (n) => `$${(n||0).toLocaleString('en-US',{minimumFractionDigits:0,maximumFractionDigits:0})}`;
const scoreColor = (s) => s >= 0.7 ? 'var(--green)' : s >= 0.4 ? 'var(--yellow)' : 'var(--red)';
const statusColor = { active:'var(--green)', paused:'var(--yellow)', stopped:'var(--red)', draft:'var(--text3)' };

// Fake sparkline data for demo
const makeSparkline = (base, count=12) =>
  Array.from({length:count},(_,i) => ({ v: base + Math.sin(i*0.8)*base*0.3 + Math.random()*base*0.1 }));

// ── Sub-components ────────────────────────────────────────────────────────────
function StatCard({ label, value, sub, color='var(--accent)', spark }) {
  return (
    <div style={{
      background:'var(--bg2)', border:'1px solid var(--border)', borderRadius:14,
      padding:'20px 22px', display:'flex', flexDirection:'column', gap:4,
    }}>
      <span style={{ fontSize:11, fontFamily:'var(--font-mono)', color:'var(--text3)', letterSpacing:1.5, textTransform:'uppercase' }}>{label}</span>
      <span style={{ fontSize:26, fontWeight:800, fontFamily:'var(--font-head)', color, lineHeight:1.1, marginTop:4 }}>{value}</span>
      {sub && <span style={{ fontSize:12, color:'var(--text3)' }}>{sub}</span>}
      {spark && (
        <div style={{ marginTop:8, height:36 }}>
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={spark}>
              <Area type="monotone" dataKey="v" stroke={color} strokeWidth={1.5} fill={`${color}18`} dot={false} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}

function CampaignRow({ c, onOptimize, optimizing }) {
  const score = c.performance_score || 0.5;
  return (
    <tr style={{ borderBottom:'1px solid var(--border)' }}>
      <td style={{ padding:'14px 16px', fontSize:13, fontWeight:600, color:'var(--text)' }}>{c.name}</td>
      <td style={{ padding:'14px 8px' }}>
        <span style={{
          fontSize:11, fontFamily:'var(--font-mono)', padding:'3px 8px', borderRadius:20,
          background:`${statusColor[c.status]||'var(--text3)'}18`,
          color: statusColor[c.status] || 'var(--text3)',
        }}>{c.status}</span>
      </td>
      <td style={{ padding:'14px 8px', fontSize:13, color:'var(--text)', fontFamily:'var(--font-mono)' }}>{fmtMoney(c.total_budget)}</td>
      <td style={{ padding:'14px 8px', fontSize:13, color:'var(--text2)', fontFamily:'var(--font-mono)' }}>{fmtMoney(c.spent_budget)}</td>
      <td style={{ padding:'14px 8px' }}>
        <div style={{ display:'flex', alignItems:'center', gap:8 }}>
          <div style={{ flex:1, height:4, background:'var(--bg3)', borderRadius:2 }}>
            <div style={{ width:`${score*100}%`, height:'100%', borderRadius:2, background:scoreColor(score) }} />
          </div>
          <span style={{ fontSize:11, fontFamily:'var(--font-mono)', color:scoreColor(score), minWidth:30 }}>{(score*100).toFixed(0)}%</span>
        </div>
      </td>
      <td style={{ padding:'14px 8px' }}>
        <button
          onClick={() => onOptimize(c.id)}
          disabled={optimizing===c.id}
          style={{
            fontSize:11, padding:'5px 12px', borderRadius:6, border:'1px solid var(--accent)',
            background: optimizing===c.id ? 'var(--bg3)' : 'rgba(0,212,255,0.1)',
            color:'var(--accent)', fontFamily:'var(--font-mono)', transition:'all .2s',
          }}
        >
          {optimizing===c.id ? '...' : '⚡ AI'}
        </button>
      </td>
    </tr>
  );
}

// ── Main Dashboard ────────────────────────────────────────────────────────────
export default function Dashboard() {
  const navigate = useNavigate();
  const [dash, setDash] = useState(null);
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [optimizing, setOptimizing] = useState(null);
  const [optResult, setOptResult] = useState(null);

  const load = async () => {
    try {
      const [dRes, cRes] = await Promise.all([dashboardAPI.overview(), campaignAPI.list()]);
      setDash(dRes.data.dashboard);
      setCampaigns(cRes.data.campaigns || []);
    } catch {}
    setLoading(false);
  };

  useEffect(() => { load(); }, []);

  const optimize = async (id) => {
    setOptimizing(id); setOptResult(null);
    try {
      const res = await campaignAPI.optimize(id);
      setOptResult({ id, actions: res.data.actions_taken });
      await load();
    } catch (e) {
      setOptResult({ id, error: 'Optimization failed' });
    }
    setOptimizing(null);
  };

  const pieData = dash ? [
    { name:'Active',   value: dash.active_campaigns  || 0, color:'var(--green)' },
    { name:'Paused',   value: dash.paused_campaigns  || 0, color:'var(--yellow)' },
    { name:'Other',    value: Math.max(0,(dash.total_campaigns||0)-((dash.active_campaigns||0)+(dash.paused_campaigns||0))), color:'var(--text3)' },
  ] : [];

  const spendData = Array.from({length:7},(_,i)=>{
    const d = new Date(); d.setDate(d.getDate()-6+i);
    return { day: d.toLocaleDateString('en',{weekday:'short'}), spend: Math.random()*2000+500, conv: Math.floor(Math.random()*40+10) };
  });

  if (loading) return (
    <div style={{display:'flex',alignItems:'center',justifyContent:'center',height:'100%',color:'var(--text3)',fontFamily:'var(--font-mono)',letterSpacing:2}}>
      LOADING...
    </div>
  );

  const d = dash || {};

  return (
    <div style={{ padding:'32px 36px', maxWidth:1200 }}>

      {/* Header */}
      <div style={{ display:'flex', justifyContent:'space-between', alignItems:'flex-start', marginBottom:32 }}>
        <div>
          <h1 style={{ fontFamily:'var(--font-head)', fontSize:28, fontWeight:800, letterSpacing:'-1px', color:'var(--text)' }}>Dashboard</h1>
          <p style={{ color:'var(--text3)', fontSize:13, marginTop:4 }}>
            {new Date().toLocaleDateString('en-US',{weekday:'long',year:'numeric',month:'long',day:'numeric'})}
          </p>
        </div>
        <button
          onClick={() => navigate('/campaigns/new')}
          style={{
            padding:'10px 20px', background:'linear-gradient(135deg,var(--accent2),var(--accent))',
            border:'none', borderRadius:10, color:'#fff', fontSize:13, fontWeight:700,
          }}
        >
          + New Campaign
        </button>
      </div>

      {/* Opt result toast */}
      {optResult && (
        <div style={{
          marginBottom:20, padding:'12px 16px', borderRadius:10,
          background: optResult.error ? 'rgba(255,69,96,0.1)' : 'rgba(0,232,143,0.1)',
          border: `1px solid ${optResult.error ? 'rgba(255,69,96,0.3)' : 'rgba(0,232,143,0.3)'}`,
          color: optResult.error ? 'var(--red)' : 'var(--green)', fontSize:13,
        }}>
          {optResult.error ? `⚠ ${optResult.error}` : `✓ AI Optimization complete — ${optResult.actions?.length||0} actions taken`}
        </div>
      )}

      {/* Stat cards */}
      <div style={{ display:'grid', gridTemplateColumns:'repeat(4,1fr)', gap:16, marginBottom:28 }}>
        <StatCard label="Total Budget"    value={fmtMoney(d.total_budget)}    sub="Across all campaigns" color="var(--accent)"  spark={makeSparkline(d.total_budget||1000)} />
        <StatCard label="Total Spent"     value={fmtMoney(d.total_spent)}     sub="Budget utilised"      color="var(--accent2)" spark={makeSparkline(d.total_spent||500)} />
        <StatCard label="Conversions"     value={fmt(d.total_conversions)}    sub="Total conversions"    color="var(--green)"   spark={makeSparkline(d.total_conversions||20)} />
        <StatCard label="Avg Performance" value={`${((d.avg_performance_score||0.5)*100).toFixed(0)}%`} sub="AI score" color={scoreColor(d.avg_performance_score||0.5)} />
      </div>

      {/* Charts row */}
      <div style={{ display:'grid', gridTemplateColumns:'2fr 1fr', gap:16, marginBottom:28 }}>

        {/* Spend chart */}
        <div style={{ background:'var(--bg2)', border:'1px solid var(--border)', borderRadius:14, padding:'20px 22px' }}>
          <div style={{ fontSize:12, fontFamily:'var(--font-mono)', color:'var(--text3)', letterSpacing:1.5, marginBottom:16, textTransform:'uppercase' }}>7-Day Spend & Conversions</div>
          <ResponsiveContainer width="100%" height={180}>
            <AreaChart data={spendData}>
              <defs>
                <linearGradient id="gSpend" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="var(--accent)" stopOpacity={0.3} />
                  <stop offset="100%" stopColor="var(--accent)" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="gConv" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="var(--green)" stopOpacity={0.3} />
                  <stop offset="100%" stopColor="var(--green)" stopOpacity={0} />
                </linearGradient>
              </defs>
              <XAxis dataKey="day" tick={{fontSize:11,fill:'var(--text3)',fontFamily:'var(--font-mono)'}} axisLine={false} tickLine={false} />
              <YAxis hide />
              <Tooltip
                contentStyle={{background:'var(--bg3)',border:'1px solid var(--border)',borderRadius:8,fontSize:12,color:'var(--text)'}}
                labelStyle={{color:'var(--text3)',fontFamily:'var(--font-mono)'}}
              />
              <Area type="monotone" dataKey="spend" stroke="var(--accent)" strokeWidth={2} fill="url(#gSpend)" name="Spend ($)" />
              <Area type="monotone" dataKey="conv"  stroke="var(--green)"  strokeWidth={2} fill="url(#gConv)"  name="Conversions" />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Pie chart */}
        <div style={{ background:'var(--bg2)', border:'1px solid var(--border)', borderRadius:14, padding:'20px 22px' }}>
          <div style={{ fontSize:12, fontFamily:'var(--font-mono)', color:'var(--text3)', letterSpacing:1.5, marginBottom:16, textTransform:'uppercase' }}>Campaign Status</div>
          {pieData.some(p=>p.value>0) ? (
            <>
              <ResponsiveContainer width="100%" height={130}>
                <PieChart>
                  <Pie data={pieData} cx="50%" cy="50%" innerRadius={40} outerRadius={60} dataKey="value" strokeWidth={0}>
                    {pieData.map((e,i) => <Cell key={i} fill={e.color} />)}
                  </Pie>
                  <Tooltip contentStyle={{background:'var(--bg3)',border:'1px solid var(--border)',borderRadius:8,fontSize:12,color:'var(--text)'}} />
                </PieChart>
              </ResponsiveContainer>
              <div style={{ display:'flex', flexDirection:'column', gap:6, marginTop:8 }}>
                {pieData.map(p => (
                  <div key={p.name} style={{ display:'flex', justifyContent:'space-between', fontSize:12 }}>
                    <span style={{ display:'flex', alignItems:'center', gap:8, color:'var(--text2)' }}>
                      <span style={{ width:8, height:8, borderRadius:'50%', background:p.color, display:'inline-block' }} />
                      {p.name}
                    </span>
                    <span style={{ fontFamily:'var(--font-mono)', color:'var(--text)' }}>{p.value}</span>
                  </div>
                ))}
              </div>
            </>
          ) : (
            <div style={{ display:'flex', alignItems:'center', justifyContent:'center', height:160, color:'var(--text3)', fontSize:13 }}>
              No campaigns yet
            </div>
          )}
        </div>
      </div>

      {/* Campaigns table */}
      <div style={{ background:'var(--bg2)', border:'1px solid var(--border)', borderRadius:14, overflow:'hidden' }}>
        <div style={{ padding:'18px 22px', borderBottom:'1px solid var(--border)', display:'flex', justifyContent:'space-between', alignItems:'center' }}>
          <span style={{ fontSize:12, fontFamily:'var(--font-mono)', color:'var(--text3)', letterSpacing:1.5, textTransform:'uppercase' }}>All Campaigns</span>
          <span style={{ fontSize:12, color:'var(--text3)' }}>{campaigns.length} total</span>
        </div>

        {campaigns.length === 0 ? (
          <div style={{ padding:60, textAlign:'center', color:'var(--text3)' }}>
            <div style={{ fontSize:40, marginBottom:12 }}>◈</div>
            <p style={{ fontSize:14 }}>No campaigns yet</p>
            <button
              onClick={() => navigate('/campaigns/new')}
              style={{ marginTop:16, padding:'8px 20px', background:'var(--bg3)', border:'1px solid var(--border)', borderRadius:8, color:'var(--accent)', fontSize:13 }}
            >
              Create your first campaign
            </button>
          </div>
        ) : (
          <div style={{ overflowX:'auto' }}>
            <table style={{ width:'100%', borderCollapse:'collapse' }}>
              <thead>
                <tr style={{ borderBottom:'1px solid var(--border)' }}>
                  {['Name','Status','Budget','Spent','AI Score','Action'].map(h => (
                    <th key={h} style={{ padding:'10px 16px', textAlign:'left', fontSize:11, fontFamily:'var(--font-mono)', color:'var(--text3)', letterSpacing:1, textTransform:'uppercase', fontWeight:500 }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {campaigns.map(c => (
                  <CampaignRow key={c.id} c={c} onOptimize={optimize} optimizing={optimizing} />
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
