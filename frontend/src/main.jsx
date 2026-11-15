import React from 'react';
import ReactDOM from 'react-dom/client';
import axios from 'axios';
import App from './App.jsx';
import './index.css';

// Configure Axios Base URL from environment variable (VITE_API_BASE_URL)
// In production on Render: e.g. https://dr-d-backend.onrender.com
// In local dev without env var: defaults to '' (uses Vite local proxy /api)
const apiBase = import.meta.env.VITE_API_BASE_URL;
if (apiBase) {
  axios.defaults.baseURL = apiBase.replace(/\/+$/, '');
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
