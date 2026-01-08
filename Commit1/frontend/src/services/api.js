/**
 * API servis - Axios konfiguracija i API pozivi
 */
import axios from 'axios';

// Bazni URL za API
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

// Kreiranje axios instance
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor - dodaje token u header
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

// Response interceptor - handle grešaka
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Token istekao ili nije validan
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

// ==================== AUTH API ====================

export const authAPI = {
    // Registracija novog korisnika
    register: async (userData) => {
        const response = await api.post('/auth/register', userData);
        return response.data;
    },

    // Prijava korisnika
    login: async (username, password) => {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        const response = await api.post('/auth/login', formData, {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        });
        return response.data;
    },

    // Odjava
    logout: async () => {
        const response = await api.post('/auth/logout');
        return response.data;
    },

    // Dobijanje trenutnog korisnika
    getMe: async () => {
        const response = await api.get('/auth/me');
        return response.data;
    },
};

// ==================== IZLOŽBE API ====================

export const izlozbeAPI = {
    // Lista izložbi sa filterima
    getAll: async (params = {}) => {
        const response = await api.get('/izlozbe', { params });
        return response.data;
    },

    // Pojedinačna izložba po ID-u
    getById: async (id) => {
        const response = await api.get(`/izlozbe/${id}`);
        return response.data;
    },

    // Pojedinačna izložba po slugu
    getBySlug: async (slug) => {
        const response = await api.get(`/izlozbe/slug/${slug}`);
        return response.data;
    },

    // Kreiranje izložbe (admin)
    create: async (data) => {
        const response = await api.post('/izlozbe', data);
        return response.data;
    },

    // Ažuriranje izložbe (admin)
    update: async (id, data) => {
        const response = await api.put(`/izlozbe/${id}`, data);
        return response.data;
    },

    // Brisanje izložbe (admin)
    delete: async (id) => {
        const response = await api.delete(`/izlozbe/${id}`);
        return response.data;
    },
};

// ==================== LOKACIJE API ====================

export const lokacijeAPI = {
    getAll: async (params = {}) => {
        const response = await api.get('/lokacije', { params });
        return response.data;
    },

    getById: async (id) => {
        const response = await api.get(`/lokacije/${id}`);
        return response.data;
    },

    create: async (data) => {
        const response = await api.post('/lokacije', data);
        return response.data;
    },

    update: async (id, data) => {
        const response = await api.put(`/lokacije/${id}`, data);
        return response.data;
    },

    delete: async (id) => {
        const response = await api.delete(`/lokacije/${id}`);
        return response.data;
    },
};

// ==================== SLIKE API ====================

export const slikeAPI = {
    getAll: async (params = {}) => {
        const response = await api.get('/slike', { params });
        return response.data;
    },

    // Dohvatanje slika sa Art Institute of Chicago
    getFromArtic: async (params = {}) => {
        const response = await api.get('/slike/artic', { params });
        return response.data;
    },

    getById: async (id) => {
        const response = await api.get(`/slike/${id}`);
        return response.data;
    },

    create: async (data) => {
        const response = await api.post('/slike', data);
        return response.data;
    },

    createFromArtic: async (artworkId) => {
        const response = await api.post(`/slike/from-artic?artwork_id=${artworkId}`);
        return response.data;
    },

    update: async (id, data) => {
        const response = await api.put(`/slike/${id}`, data);
        return response.data;
    },

    delete: async (id) => {
        const response = await api.delete(`/slike/${id}`);
        return response.data;
    },
};

// ==================== PRIJAVE API ====================

export const prijaveAPI = {
    // Lista svih prijava (admin)
    getAll: async (params = {}) => {
        const response = await api.get('/prijave', { params });
        return response.data;
    },

    // Moje prijave
    getMoje: async () => {
        const response = await api.get('/prijave/moje');
        return response.data;
    },

    // Pojedinačna prijava
    getById: async (id) => {
        const response = await api.get(`/prijave/${id}`);
        return response.data;
    },

    // Kreiranje prijave
    create: async (data) => {
        const response = await api.post('/prijave', data);
        return response.data;
    },

    // Validacija QR koda
    validate: async (qrKod) => {
        const response = await api.post('/prijave/validate', { qr_kod: qrKod });
        return response.data;
    },

    // Otkazivanje prijave
    delete: async (id) => {
        const response = await api.delete(`/prijave/${id}`);
        return response.data;
    },
};

// ==================== KORISNICI API ====================

export const korisniciAPI = {
    getAll: async (params = {}) => {
        const response = await api.get('/korisnici', { params });
        return response.data;
    },

    getById: async (id) => {
        const response = await api.get(`/korisnici/${id}`);
        return response.data;
    },

    update: async (id, data) => {
        const response = await api.put(`/korisnici/${id}`, data);
        return response.data;
    },

    delete: async (id) => {
        const response = await api.delete(`/korisnici/${id}`);
        return response.data;
    },
};

export default api;
