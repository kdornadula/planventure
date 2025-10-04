import axios from "axios";

// Create axios instance with base configuration
const api = axios.create({
  baseURL:
    process.env.NODE_ENV === "production"
      ? "https://your-api-domain.com" // Replace with your production API URL
      : "http://localhost:5000", // Development API URL
  headers: {
    "Content-Type": "application/json",
  },
});

// Add token to requests automatically
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
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
      // Token expired or invalid
      localStorage.removeItem("access_token");
      localStorage.removeItem("user");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

// Authentication API calls
export const authAPI = {
  register: (userData) => api.post("/auth/register", userData),
  login: (credentials) => api.post("/auth/login", credentials),
  validateEmail: (email) => api.post("/auth/validate-email", { email }),
};

// Trips API calls
export const tripsAPI = {
  getTrips: (params = {}) => api.get("/trips", { params }),
  getTrip: (id) => api.get(`/trips/${id}`),
  createTrip: (tripData) => api.post("/trips", tripData),
  updateTrip: (id, tripData) => api.put(`/trips/${id}`, tripData),
  deleteTrip: (id) => api.delete(`/trips/${id}`),
  searchTrips: (params) => api.get("/trips/search", { params }),
  getTemplate: (params) => api.get("/trips/template", { params }),
  getWeekendTemplate: (destination) =>
    api.get("/trips/template/weekend", { params: { destination } }),
  getBusinessTemplate: (destination, duration) =>
    api.get("/trips/template/business", { params: { destination, duration } }),
  getSuggestions: (destination) => api.get(`/trips/suggestions/${destination}`),
};

// Health check
export const healthAPI = {
  check: () => api.get("/health"),
  simple: () => api.get("/health/simple"),
  database: () => api.get("/health/database"),
};

export default api;
