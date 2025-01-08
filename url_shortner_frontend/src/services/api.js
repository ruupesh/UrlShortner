import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL
const api = axios.create({
  baseURL: API_BASE_URL,
});

// Authentication APIs
export const login = (data) => api.post('/api/token/', data);
export const refreshToken = (data) => api.post('/api/token/refresh/', data);
export const register = (data) => api.post('/api/register/', data);

// Logout (clear token client-side)
export const logout = () => {
  localStorage.removeItem('token');
};

// Shorten URL
export const shortenURL = (data, token) =>
  api.post('/api/shorten/', data, {
    headers: { Authorization: `Bearer ${token}` },
  });

// Get Analytics
export const getAnalytics = (token) =>
  api.get('/api/analytics/', {
    headers: { Authorization: `Bearer ${token}` },
  });

export const deleteURL = (shortUrl, token) =>
    api.delete('/api/analytics/', {
        headers: { Authorization: `Bearer ${token}` },
        data: { short_url: shortUrl }, // Include short_url in the request body
    });
  

export default api;
