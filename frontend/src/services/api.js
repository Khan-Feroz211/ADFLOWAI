// ADFLOWAI - API Service
// All communication with the Flask backend

import axios from 'axios';

const BASE = process.env.REACT_APP_API_BASE_URL || '/api/v1';

// ── Axios instance ────────────────────────────────────────────────────────────
const api = axios.create({ baseURL: BASE });

// Attach JWT token to every request automatically
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  config.headers = config.headers || {};
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// If token expired, redirect to login
api.interceptors.response.use(
  (r) => r,
  async (err) => {
    const original = err.config || {};
    const refreshToken = localStorage.getItem('refresh_token');
    const status = err.response?.status;
    const isRefreshRequest = original.url?.includes('/auth/refresh');

    // Try one automatic refresh before forcing logout.
    if (status === 401 && refreshToken && !original._retry && !isRefreshRequest) {
      original._retry = true;
      try {
        const refreshRes = await axios.post(
          `${BASE}/auth/refresh`,
          {},
          { headers: { Authorization: `Bearer ${refreshToken}` } }
        );
        const newAccess = refreshRes.data?.access_token;
        if (newAccess) {
          localStorage.setItem('access_token', newAccess);
          original.headers = original.headers || {};
          original.headers.Authorization = `Bearer ${newAccess}`;
          return api(original);
        }
      } catch (_) {
        // Fall through to logout path.
      }
    }

    if (status === 401) {
      localStorage.clear();
      window.location.href = '/login';
    }
    return Promise.reject(err);
  }
);

// ── Auth ──────────────────────────────────────────────────────────────────────
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  me: () => api.get('/auth/me'),
  logout: () => api.post('/auth/logout'),
};

// ── Campaigns ─────────────────────────────────────────────────────────────────
export const campaignAPI = {
  list: (status) => api.get('/campaigns', { params: status ? { status } : {} }),
  get: (id) => api.get(`/campaigns/${id}`),
  create: (data) => api.post('/campaigns', data),
  delete: (id) => api.delete(`/campaigns/${id}`),
  updateMetrics: (id, metrics) => api.post(`/campaigns/${id}/metrics`, metrics),
  optimize: (id) => api.post(`/campaigns/${id}/optimize`),
  analytics: (id) => api.get(`/campaigns/${id}/analytics`),
};

// ── Dashboard ─────────────────────────────────────────────────────────────────
export const dashboardAPI = {
  overview: () => api.get('/dashboard'),
  platforms: () => api.get('/platforms'),
};

export default api;
