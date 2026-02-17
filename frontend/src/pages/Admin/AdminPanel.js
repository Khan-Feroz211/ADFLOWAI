import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';

const s = {
  page: { padding:'32px 36px', maxWidth:1100 },
  h1:   { fontFamily:'var(--font-head)', fontSize:28, fontWeight:800, letterSpacing:'-1px', marginBottom:4 },
  sub:  { color:'var(--text3)', fontSize:13, marginBottom:32 },
  grid: { display:'grid', gridTemplateColumns:'repeat(4,1fr)', gap:14, marginBottom:28 },
  card: { background:'var(--bg2)', border:'1px solid var(--border)', borderRadius:12, padding:'18px 20px' },
  lbl:  { fontSize:10, fontFamily:'var(--font-mono)', color:'var(--text3)', letterSpacing:2, textTransform:'uppercase', marginBottom:6 },
  val:  { fontFamily:'var(--font-head)', fontSize:26, fontWeight:800 },
  sub2: { fontSize:11, color:'var(--text3)', marginTop:4 },
  table: { width:'100%', borderCollapse:'collapse' },
  th:   { padding:'10px 14px', textAlign:'left', fontSize:11, fontFamily:'var(--font-mono)', color:'var(--text3)', letterSpacing:1, textTransform:'uppercase', borderBottom:'1px solid var(--border)', fontWeight:400 },
  td:   { padding:'12px 14px', fontSize:13, borderBottom:'1px solid var(--border)' },
  badge:(c)=>({ fontSize:10, padding:'2px 8px', borderRadius:20, background:`${c}22`, color:c, fontFamily:'var(--font-mono)' }),
  btn:  (c='var(--accent)')=>({ padding:'4px 12px', borderRadius:6, border:`1px solid ${c}`, background:`${c}18`, color:c, fontSize:11, fontFamily:'var(--font-mono)', cursor:'pointer' }),
  toast:(t)=>({ position:'fixed', top:24, right:24, zIndex:999, padding:'12px 20px', borderRadius:10, fontSize:13, fontWeight:600, background: t==='ok'?'rgba(0,232,143,0.15)':'rgba(255,69,96,0.15)', border:`1px solid ${t==='ok'?'rgba(0,232,143,0.4)':'rgba(255,69,96,0.4)'}`, color: t==='ok'?'var(--green)':'var(--red)' }),
};

export default function AdminPanel() {
  const navigate = useNavigate();
  const user     = JSON.parse(localStorage.getItem('user') || '{}');
  const [stats,  setStats]  = useState(null);
  const [users,  setUsers]  = useState([]);
  const [search, setSearch] = useState('');
  const [page,   setPage]   = useState(1);
  const [total,  setTotal]  = useState(0);
  const [pages,  setPages]  = useState(1);
  const [toast,  setToast]  = useState(null);
  const [loading,setLoading]= useState(true);

  // Redirect if not admin
  useEffect(() => {
    if (user.role !== 'admin') { navigate('/'); }
  }, []);

  const showToast = (msg, type='ok') => {
    setToast({msg,type});
    setTimeout(() => setToast(null), 3000);
  };

  const loadData = async (p=1, s=search) => {
    setLoading(true);
    try {
      const [statsRes, usersRes] = await Promise.all([
        api.get('/admin/stats'),
        api.get(`/admin/users?page=${p}&per_page=10${s?`&search=${s}`:''}`)
      ]);
      setStats(statsRes.data.stats);
      setUsers(usersRes.data.users);
      setTotal(usersRes.data.total);
      setPages(usersRes.data.pages);
    } catch (e) {
      if (e.response?.status === 403) {
        showToast('Admin access required', 'err');
        navigate('/');
      }
    }
    setLoading(false);
  };

  useEffect(() => { loadData(); }, []);

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
    if (!window.confirm('Delete this user? This also deletes all their campaigns.')) return;
    try {
      await api.delete(`/admin/users/${id}`);
      showToast('User deleted');
      loadData(page);
    } catch { showToast('Failed', 'err'); }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    setPage(1);
    loadData(1, search);
  };

  const st = stats || {};
  const statCards = [
    { label:'Total Users',    val: st.users?.total || 0,              sub: `${st.users?.new_this_week||0} new this week`,  color:'var(--accent)' },
    { label:'Active Users',   val: st.users?.active || 0,             sub: `${st.users?.inactive||0} inactive`,            color:'var(--green)' },
    { label:'Total Campaigns',val: st.campaigns?.total || 0,          sub: `${st.campaigns?.active||0} active`,            color:'var(--accent2)' },
    { label:'Budget Managed', val: `$${((st.financials?.total_budget_managed||0)/1000).toFixed(0)}K`, sub:'Total across all users', color:'var(--yellow)' },
  ];

  return (
    <div style={s.page}>
      {toast && <div style={s.toast(toast.type)}>{toast.type==='ok'?'✓':'⚠'} {toast.msg}</div>}

      <h1 style={s.h1}>Admin Panel</h1>
      <p style={s.sub}>System overview and user management</p>

      {/* Stat cards */}
      <div style={s.grid}>
        {statCards.map(c => (
          <div key={c.label} style={s.card}>
            <div style={s.lbl}>{c.label}</div>
            <div style={{...s.val, color:c.color}}>{c.val}</div>
            <div style={s.sub2}>{c.sub}</div>
          </div>
        ))}
      </div>

      {/* AI Stats */}
      <div style={{...s.card, marginBottom:28, display:'flex', gap:40}}>
        <div>
          <div style={s.lbl}>Total AI Optimizations</div>
          <div style={{...s.val, fontSize:20, color:'var(--green)'}}>{st.ai?.total_optimizations || 0}</div>
        </div>
        <div>
          <div style={s.lbl}>Avg Budget / Campaign</div>
          <div style={{...s.val, fontSize:20}}>${(st.financials?.avg_budget||0).toLocaleString()}</div>
        </div>
        <div>
          <div style={s.lbl}>Total Spent</div>
          <div style={{...s.val, fontSize:20, color:'var(--yellow)'}}>${(st.financials?.total_spent||0).toLocaleString()}</div>
        </div>
      </div>

      {/* Users table */}
      <div style={{ background:'var(--bg2)', border:'1px solid var(--border)', borderRadius:14, overflow:'hidden' }}>
        <div style={{ padding:'16px 20px', borderBottom:'1px solid var(--border)', display:'flex', justifyContent:'space-between', alignItems:'center', gap:16 }}>
          <span style={{ fontSize:11, fontFamily:'var(--font-mono)', color:'var(--text3)', letterSpacing:2, textTransform:'uppercase' }}>
            Users ({total})
          </span>
          <form onSubmit={handleSearch} style={{ display:'flex', gap:8 }}>
            <input
              value={search} onChange={e=>setSearch(e.target.value)}
              placeholder="Search users..." 
              style={{ padding:'6px 12px', background:'var(--bg3)', border:'1px solid var(--border)', borderRadius:8, color:'var(--text)', fontSize:13, outline:'none', width:200 }}
            />
            <button type="submit" style={s.btn()}>Search</button>
            {search && <button type="button" style={s.btn('var(--text3)')} onClick={() => { setSearch(''); loadData(1,''); }}>Clear</button>}
          </form>
        </div>

        {loading ? (
          <div style={{ padding:40, textAlign:'center', color:'var(--text3)', fontFamily:'var(--font-mono)' }}>LOADING...</div>
        ) : users.length === 0 ? (
          <div style={{ padding:40, textAlign:'center', color:'var(--text3)' }}>No users found</div>
        ) : (
          <div style={{ overflowX:'auto' }}>
            <table style={s.table}>
              <thead>
                <tr>
                  {['User','Email','Company','Role','Status','Campaigns','Last Login','Actions'].map(h=>(
                    <th key={h} style={s.th}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {users.map(u => (
                  <tr key={u.id} style={{ opacity: u.is_active?1:0.5 }}>
                    <td style={s.td}>
                      <div style={{ fontWeight:600 }}>{u.username}</div>
                      <div style={{ fontSize:11, color:'var(--text3)' }}>ID: {u.id}</div>
                    </td>
                    <td style={{...s.td, color:'var(--text2)', fontSize:12}}>{u.email}</td>
                    <td style={{...s.td, color:'var(--text2)', fontSize:12}}>{u.company || '—'}</td>
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
                    <td style={{...s.td, fontFamily:'var(--font-mono)', textAlign:'center'}}>{u.campaign_count}</td>
                    <td style={{...s.td, fontSize:11, color:'var(--text3)'}}>
                      {u.last_login ? new Date(u.last_login).toLocaleDateString() : 'Never'}
                    </td>
                    <td style={s.td}>
                      <div style={{ display:'flex', gap:6, flexWrap:'wrap' }}>
                        <button style={s.btn(u.is_active?'var(--yellow)':'var(--green)')} onClick={()=>toggleActive(u.id)}>
                          {u.is_active?'Disable':'Enable'}
                        </button>
                        {u.role !== 'admin' && (
                          <button style={s.btn('var(--accent)')} onClick={()=>setRole(u.id,'admin')}>
                            Make Admin
                          </button>
                        )}
                        {u.role === 'admin' && u.id !== (JSON.parse(localStorage.getItem('user')||'{}').id) && (
                          <button style={s.btn('var(--text3)')} onClick={()=>setRole(u.id,'user')}>
                            Remove Admin
                          </button>
                        )}
                        {u.id !== (JSON.parse(localStorage.getItem('user')||'{}').id) && (
                          <button style={s.btn('var(--red)')} onClick={()=>deleteUser(u.id)}>Delete</button>
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
          <div style={{ padding:'12px 20px', borderTop:'1px solid var(--border)', display:'flex', gap:8, justifyContent:'center' }}>
            {Array.from({length:pages},(_,i)=>i+1).map(p=>(
              <button key={p} onClick={()=>{ setPage(p); loadData(p); }}
                style={{ ...s.btn(p===page?'var(--accent)':'var(--text3)'), minWidth:32 }}>
                {p}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
