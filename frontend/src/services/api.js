import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API_BASE = `${BACKEND_URL}/api`;

// Create axios instance
const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (userData) => api.post('/auth/register', userData),
  login: (credentials) => api.post('/auth/login', credentials),
  logout: () => api.post('/auth/logout'),
  getProfile: () => api.get('/auth/profile'),
  updateProfile: (updates) => api.put('/auth/profile', updates),
};

// Destinations API
export const destinationsAPI = {
  getAll: () => api.get('/destinations'),
  getBySlug: (slug) => api.get(`/destinations/${slug}`),
  getProperties: (slug) => api.get(`/destinations/${slug}/properties`),
};

// Properties API
export const propertiesAPI = {
  getAll: (params = {}) => api.get('/properties', { params }),
  search: (filters = {}) => api.get('/properties/search', { params: filters }),
  getById: (id) => api.get(`/properties/${id}`),
  create: (propertyData) => api.post('/properties', propertyData),
  update: (id, updates) => api.put(`/properties/${id}`, updates),
  delete: (id) => api.delete(`/properties/${id}`),
};

// Bookings API
export const bookingsAPI = {
  create: (bookingData) => api.post('/bookings', bookingData),
  getAll: () => api.get('/bookings'),
  getById: (id) => api.get(`/bookings/${id}`),
  update: (id, updates) => api.put(`/bookings/${id}`, updates),
  cancel: (id) => api.delete(`/bookings/${id}`),
  processPayment: (id) => api.post(`/bookings/${id}/payment`),
};

// Blog API
export const blogAPI = {
  getPosts: (params = {}) => api.get('/blog/posts', { params }),
  getPost: (slug) => api.get(`/blog/posts/${slug}`),
};

// Content API
export const contentAPI = {
  getInspiration: () => api.get('/inspiration'),
  getSpecialOffers: (activeOnly = true) => api.get('/special-offers', { 
    params: { active_only: activeOnly } 
  }),
};

// Reviews API
export const reviewsAPI = {
  getPropertyReviews: (propertyId) => api.get(`/properties/${propertyId}/reviews`),
  createReview: (propertyId, reviewData) => api.post(`/properties/${propertyId}/reviews`, reviewData),
  getReview: (id) => api.get(`/reviews/${id}`),
  updateReview: (id, updates) => api.put(`/reviews/${id}`, updates),
  deleteReview: (id) => api.delete(`/reviews/${id}`),
};

export default api;