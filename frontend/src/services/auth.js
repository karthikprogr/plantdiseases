import api from './api';

export const authService = {
    login: async (username, password) => {
        const response = await api.post('/auth/login', { username, password });
        if (response.data.token) {
            localStorage.setItem('token', response.data.token);
            localStorage.setItem('username', response.data.username);
        }
        return response.data;
    },

    signup: async (username, password) => {
        const response = await api.post('/auth/signup', { username, password });
        return response.data;
    },

    logout: () => {
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        window.location.href = '/login';
    },

    isAuthenticated: () => {
        return !!localStorage.getItem('token');
    },

    getUsername: () => {
        return localStorage.getItem('username');
    },
};
