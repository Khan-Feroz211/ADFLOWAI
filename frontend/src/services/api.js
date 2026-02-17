// ADFLOWAI - API Service
// All communication with the Flask backend

import axios from 'axios';

const BASE = '/api/v1';

// ── Axios instance ────────────────────────────────────────────────────────────
const api = axios.create({ baseURL: BASE });

// Attach JWT token to every request automatically
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// If token expired, redirect to login
api.interceptors.response.use(
  (r) => r,
  (err) => {
    if (err.response?.status === 401) {
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
