import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';

const s = {
  page:  { padding:'32px 36px', maxWidth:1100 },
  h1:    { fontFamily:'var(--font-head)', fontSize:28, fontWeight:800, letterSpacing:'-1px', marginBottom:4 },
  sub:   { color:'var(--text3)', fontSize:13, marginBottom:28 },
  grid:  { display:'grid', gridTemplateColumns:'repeat(4,1fr)', gap:14, marginBottom:28 },
  card:  { background:'var(--bg2)', border:'1px solid var(--border)', borderRadius:12, padding:'18px 20px' },
  lbl:   { fontSize:10, fontFamily:'var(--font-mono)', color:'var(--text3)', letterSpacing:2, textTransform:'uppercase', marginBottom:6 },
  val:   { fontFamily:'var(--font-head)', fontSize:26, fontWeight:800 },
  sub2:  { fontSize:11, color:'var(--text3)', marginTop:4 },
  table: { width:'100%', borderCollapse:'collapse' },
  th:    { padding:'10px 14px', textAlign:'left', fontSize:11, fontFamily:'var(--font-mono)', color:'var(--text3)', letterSpacing:1, textTransform:'uppercase', borderBottom:'1px solid var(--border)', fontWeight:400 },
  td:    { padding:'12px 14px', fontSize:13, borderBottom:'1px solid var(--border)' },
  badge: (c) => ({ fontSize:10, padding:'2px 8px', borderRadius:20, background:`${c}22`, color:c, fontFamily:'var(--font-mono)' }),
  btn:   (c='var(--accent)') => ({ padding:'5px 12px', borderRadius:6, border:`1px solid ${c}`, background:`${c}18`, color:c, fontSize:11, fontFamily:'var(--font-mono)', cursor:'pointer' }),
  notAdmin: { maxWidth:500, margin:'80px auto', textAlign:'center', padding:40, background:'var(--bg2)', border:'1px solid var(--border)', borderRadius:16 },
};

export default function AdminPanel() {
  const navigate  = useNavigate();
  const [myRole,  setMyRole]    = useState(null);  // fetched fresh from API
  const [stats,   setStats]     = useState(null);
  const [users,   setUsers]     = useState([]);
  const [search,  setSearch]    = useState('');
  const [page,    setPage]      = useState(1);
  const [total,   setTotal]     = useState(0);
  const [pages,   setPages]     = useState(1);
  const [toast,   setToast]     = useState(null);
  const [loading, setLoading]   = useState(true);
  const [bootstrapping, setBootstrapping] = useState(false);

  const showToast = (msg, type='ok') => {
    setToast({ msg, type });
    setTimeout(() => setToast(null), 3500);
  };

  // Step 1: Always fetch fresh role from API (not stale localStorage)
  useEffect(() => {
    api.get('/auth/me').then(res => {
      const role = res.data.user.role;
      setMyRole(role);
      // Also update localStorage so sidebar shows correctly
      const stored = JSON.parse(localStorage.getItem('user') || '{}');
      localStorage.setItem('user', JSON.stringify({ ...stored, role }));
      if (role === 'admin') loadData();
      else setLoading(false);
    }).catch(() => {
      navigate('/login');
    });
  }, []);

  const loadData = async (p = 1, s = search) => {
    setLoading(true);
    try {
      const [statsRes, usersRes] = await Promise.all([
        api.get('/admin/stats'),
        api.get(`/admin/users?page=${p}&per_page=10${s ? `&search=${encodeURIComponent(s)}` : ''}`),
      ]);
      setStats(statsRes.data.stats);
      setUsers(usersRes.data.users || []);
      setTotal(usersRes.data.total || 0);
      setPages(usersRes.data.pages || 1);
    } catch (e) {
      showToast('Failed to load admin data', 'err');
    }
    setLoading(false);
  };

  const bootstrap = async () => {
    setBootstrapping(true);
    try {
      const res = await api.post('/admin/bootstrap');
      showToast(res.data.message);
      // Re-fetch role
      const meRes = await api.get('/auth/me');
      const role  = meRes.data.user.role;
      setMyRole(role);
      const stored = JSON.parse(localStorage.getItem('user') || '{}');
      localStorage.setItem('user', JSON.stringify({ ...stored, role }));
      if (role === 'admin') loadData();
    } catch (e) {
      showToast(e.response?.data?.error || 'Bootstrap failed', 'err');
    }
    setBootstrapping(false);
  };

  const toggleActive = async (id) => {
    try {
      const res = await api.post(`/admin/users/${id}/toggle-active`);
      showToast(res.data.message);
      loadData(page);
    } catch { showToast('Failed', 'err'); }
  };

  const setRole = async (id, role) => {
    try {
      await api.post(`/admin/users/${id}/role`, { role });
      showToast(`Role set to ${role}`);
      loadData(page);
    } catch { showToast('Failed', 'err'); }
  };

  const deleteUser = async (id) => {
    if (!window.confirm('Delete this user and all their campaigns?')) return;
    try {
      await api.delete(`/admin/users/${id}`);
      showToast('User deleted');
      loadData(page);
    } catch { showToast('Failed', 'err'); }
  };

  const myUserId = JSON.parse(localStorage.getItem('user') || '{}').id;

  // ── Loading state ──────────────────────────────────────────────────────────
  if (myRole === null) {
    return (
      <div style={{ display:'flex', alignItems:'center', justifyContent:'center', height:'60vh', color:'var(--text3)', fontFamily:'var(--font-mono)', letterSpacing:2 }}>
        CHECKING PERMISSIONS...
      </div>
    );
  }

  // ── Not admin yet: show bootstrap option ──────────────────────────────────
  if (myRole !== 'admin') {
    return (
      <div style={s.notAdmin}>
        <div style={{ fontSize:48, marginBottom:16 }}>⚙</div>
        <h2 style={{ fontFamily:'var(--font-head)', fontSize:22, fontWeight:800, marginBottom:8 }}>Admin Access Required</h2>
        <p style={{ color:'var(--text3)', fontSize:13, lineHeight:1.7, marginBottom:24 }}>
          Your account doesn't have admin privileges yet.<br />
          If you're the first user, click below to make yourself admin.
        </p>
        <button
          onClick={bootstrap}
          disabled={bootstrapping}
          style={{
            padding:'12px 28px', background:'linear-gradient(135deg,var(--accent2),var(--accent))',
            border:'none', borderRadius:10, color:'#fff', fontSize:14, fontWeight:700, cursor:'pointer',
            opacity: bootstrapping ? 0.7 : 1,
          }}
        >
          {bootstrapping ? 'Promoting...' : '⚡ Make Me Admin'}
        </button>
        <p style={{ color:'var(--text3)', fontSize:11, marginTop:16, fontFamily:'var(--font-mono)' }}>
          This only works if no admin exists yet
        </p>
      </div>
    );
  }

  // ── Admin dashboard ────────────────────────────────────────────────────────
  const st = stats || {};
  const statCards = [
    { label:'Total Users',     val: st.users?.total || 0,        sub:`${st.users?.new_this_week||0} new this week`,  color:'var(--accent)' },
    { label:'Active Users',    val: st.users?.active || 0,       sub:`${st.users?.inactive||0} inactive`,            color:'var(--green)' },
    { label:'Total Campaigns', val: st.campaigns?.total || 0,    sub:`${st.campaigns?.active||0} active`,            color:'var(--accent2)' },
    { label:'Budget Managed',  val: `$${((st.financials?.total_budget_managed||0)/1000).toFixed(1)}K`, sub:'All users combined', color:'var(--yellow)' },
  ];

  return (
    <div style={s.page}>

      {/* Toast */}
      {toast && (
        <div style={{ position:'fixed', top:24, right:24, zIndex:999, padding:'12px 20px', borderRadius:10, fontSize:13, fontWeight:600, background: toast.type==='ok'?'rgba(0,232,143,0.15)':'rgba(255,69,96,0.15)', border:`1px solid ${toast.type==='ok'?'rgba(0,232,143,0.4)':'rgba(255,69,96,0.4)'}`, color: toast.type==='ok'?'var(--green)':'var(--red)', boxShadow:'0 8px 32px rgba(0,0,0,0.4)' }}>
          {toast.type==='ok'?'✓':'⚠'} {toast.msg}
        </div>
      )}

      <h1 style={s.h1}>Admin Panel</h1>
      <p style={s.sub}>System overview and user management · Logged in as admin</p>

      {/* Stat cards */}
      <div style={s.grid}>
        {statCards.map(c => (
          <div key={c.label} style={s.card}>
            <div style={s.lbl}>{c.label}</div>
            <div style={{ ...s.val, color:c.color }}>{c.val}</div>
            <div style={s.sub2}>{c.sub}</div>
          </div>
        ))}
      </div>

      {/* Extra stats bar */}
      <div style={{ ...s.card, marginBottom:28, display:'flex', gap:48, flexWrap:'wrap' }}>
        <div><div style={s.lbl}>AI Optimizations Run</div><div style={{ ...s.val, fontSize:20, color:'var(--green)' }}>{st.ai?.total_optimizations||0}</div></div>
        <div><div style={s.lbl}>Avg Budget / Campaign</div><div style={{ ...s.val, fontSize:20 }}>${(st.financials?.avg_budget||0).toLocaleString()}</div></div>
        <div><div style={s.lbl}>Total Ad Spend</div><div style={{ ...s.val, fontSize:20, color:'var(--yellow)' }}>${(st.financials?.total_spent||0).toLocaleString()}</div></div>
        <div><div style={s.lbl}>New Campaigns (7d)</div><div style={{ ...s.val, fontSize:20, color:'var(--accent2)' }}>{st.campaigns?.new_this_week||0}</div></div>
      </div>

      {/* Users table */}
      <div style={{ background:'var(--bg2)', border:'1px solid var(--border)', borderRadius:14, overflow:'hidden' }}>

        {/* Table header + search */}
        <div style={{ padding:'16px 20px', borderBottom:'1px solid var(--border)', display:'flex', justifyContent:'space-between', alignItems:'center', gap:16, flexWrap:'wrap' }}>
          <span style={{ fontSize:11, fontFamily:'var(--font-mono)', color:'var(--text3)', letterSpacing:2, textTransform:'uppercase' }}>
            All Users ({total})
          </span>
          <form onSubmit={(e)=>{ e.preventDefault(); setPage(1); loadData(1,search); }} style={{ display:'flex', gap:8 }}>
            <input
              value={search} onChange={e=>setSearch(e.target.value)}
              placeholder="Search by name, email, company..."
              style={{ padding:'7px 12px', background:'var(--bg3)', border:'1px solid var(--border)', borderRadius:8, color:'var(--text)', fontSize:13, outline:'none', width:240 }}
            />
            <button type="submit" style={s.btn()}>Search</button>
            {search && (
              <button type="button" style={s.btn('var(--text3)')} onClick={()=>{ setSearch(''); loadData(1,''); }}>
                Clear
              </button>
            )}
          </form>
        </div>

        {/* Table body */}
        {loading ? (
          <div style={{ padding:48, textAlign:'center', color:'var(--text3)', fontFamily:'var(--font-mono)', letterSpacing:2 }}>LOADING...</div>
        ) : users.length === 0 ? (
          <div style={{ padding:48, textAlign:'center', color:'var(--text3)' }}>No users found</div>
        ) : (
          <div style={{ overflowX:'auto' }}>
            <table style={s.table}>
              <thead>
                <tr>
                  {['User','Email','Company','Role','Status','Campaigns','Last Login','Actions'].map(h => (
                    <th key={h} style={s.th}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {users.map(u => (
                  <tr key={u.id} style={{ borderBottom:'1px solid var(--border)', opacity:u.is_active?1:0.5 }}>
                    <td style={s.td}>
                      <div style={{ fontWeight:600, color:'var(--text)' }}>{u.username}</div>
                      <div style={{ fontSize:11, color:'var(--text3)', fontFamily:'var(--font-mono)' }}>#{u.id}</div>
                    </td>
                    <td style={{ ...s.td, color:'var(--text2)', fontSize:12 }}>{u.email}</td>
                    <td style={{ ...s.td, color:'var(--text2)', fontSize:12 }}>{u.company||'—'}</td>
                    <td style={s.td}>
                      <span style={s.badge(u.role==='admin'?'var(--accent)':u.role==='agency'?'var(--accent2)':'var(--text3)')}>
                        {u.role}
                      </span>
                    </td>
                    <td style={s.td}>
                      <span style={s.badge(u.is_active?'var(--green)':'var(--red)')}>
                        {u.is_active?'active':'inactive'}
                      </span>
                    </td>
                    <td style={{ ...s.td, fontFamily:'var(--font-mono)', textAlign:'center' }}>{u.campaign_count}</td>
                    <td style={{ ...s.td, fontSize:11, color:'var(--text3)' }}>
                      {u.last_login ? new Date(u.last_login).toLocaleDateString('en-GB') : 'Never'}
                    </td>
                    <td style={s.td}>
                      <div style={{ display:'flex', gap:6, flexWrap:'wrap' }}>
                        {u.id !== myUserId && (
                          <button style={s.btn(u.is_active?'var(--yellow)':'var(--green)')} onClick={()=>toggleActive(u.id)}>
                            {u.is_active?'Disable':'Enable'}
                          </button>
                        )}
                        {u.role !== 'admin' && (
                          <button style={s.btn('var(--accent)')} onClick={()=>setRole(u.id,'admin')}>→ Admin</button>
                        )}
                        {u.role === 'admin' && u.id !== myUserId && (
                          <button style={s.btn('var(--text3)')} onClick={()=>setRole(u.id,'user')}>→ User</button>
                        )}
                        {u.id !== myUserId && (
                          <button
                            style={s.btn('var(--red)')}
                            onClick={()=>deleteUser(u.id)}
                          >✕</button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Pagination */}
        {pages > 1 && (
          <div style={{ padding:'14px 20px', borderTop:'1px solid var(--border)', display:'flex', gap:6, justifyContent:'center' }}>
            <button onClick={()=>{ setPage(p=>Math.max(1,p-1)); loadData(Math.max(1,page-1)); }} disabled={page===1} style={s.btn('var(--text3)')}>←</button>
            {Array.from({length:pages},(_,i)=>i+1).map(p=>(
              <button key={p} onClick={()=>{ setPage(p); loadData(p); }} style={s.btn(p===page?'var(--accent)':'var(--text3)')}>
                {p}
              </button>
            ))}
            <button onClick={()=>{ setPage(p=>Math.min(pages,p+1)); loadData(Math.min(pages,page+1)); }} disabled={page===pages} style={s.btn('var(--text3)')}>→</button>
          </div>
        )}
      </div>
    </div>
  );
}
