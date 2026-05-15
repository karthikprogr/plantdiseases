import axios from 'axios';

// Use environment variable for API URL, fallback to localhost
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true, // Enable cookies for session management
});

// Add token to requests if it exists (JWT or Firebase token)
api.interceptors.request.use(async (config) => {
    // Try to get Firebase token first
    try {
        const { auth } = await import('../firebase');
        const user = auth.currentUser;
        if (user) {
            const token = await user.getIdToken();
            config.headers.Authorization = `Bearer ${token}`;
            return config;
        }
    } catch (error) {
        console.log('Firebase not initialized or user not logged in');
    }
    
    // Fallback to localStorage token (for backward compatibility)
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Handle token expiration
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('token');
            localStorage.removeItem('username');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export default api;
