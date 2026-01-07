import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

// Interceptor to add the Role header dynamically
api.interceptors.request.use((config) => {
  const role = localStorage.getItem('user_role') || 'user';
  config.headers['x-role'] = role;
  return config;
});

export default api;