// src/utils/api.js
import axios from 'axios';

export const api = axios.create({
  baseURL: 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add request interceptor to add token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('userId');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Add to api.js
api.interceptors.response.use(
  response => response,
  error => {
      console.error('API Error:', {
          endpoint: error.config.url,
          method: error.config.method,
          status: error.response?.status,
          error: error.response?.data?.error
      });
      return Promise.reject(error);
  }
);