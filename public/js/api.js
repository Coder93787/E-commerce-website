/**
 * API Client for VERDANT Store Backend
 */
const API = {
  baseUrl: window.location.origin,

  getToken() {
    return localStorage.getItem('verdant_token');
  },

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    };

    const token = this.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers
      });

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(data.error || `HTTP error! Status: ${response.status}`);
      }

      return data;
    } catch (err) {
      console.error(`API Error on ${endpoint}:`, err);
      throw err;
    }
  },

  // Products
  getProducts(category, search, sort) {
    const params = new URLSearchParams();
    if (category && category !== 'All') params.append('category', category);
    if (search) params.append('search', search);
    if (sort) params.append('sort', sort);
    return this.request(`/api/products?${params.toString()}`);
  },

  getProduct(id) {
    return this.request(`/api/products/${id}`);
  },

  getCategories() {
    return this.request('/api/categories');
  },

  // Auth
  register(name, email, password) {
    return this.request('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify({ name, email, password })
    });
  },

  login(email, password) {
    return this.request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    });
  },

  getMe() {
    return this.request('/api/auth/me');
  },

  logout() {
    return this.request('/api/auth/logout', { method: 'POST' });
  },

  // Payments & Checkout
  processPayment(payload) {
    return this.request('/api/payments/process', {
      method: 'POST',
      body: JSON.stringify(payload)
    });
  },

  // Orders
  getMyOrders() {
    return this.request('/api/orders/my-orders');
  },

  // Admin
  getAdminMetrics() {
    return this.request('/api/admin/metrics');
  },

  getAdminOrders() {
    return this.request('/api/admin/orders');
  },

  updateOrderStatus(orderId, status) {
    return this.request(`/api/admin/orders/${orderId}/status`, {
      method: 'PUT',
      body: JSON.stringify({ status })
    });
  },

  createProduct(productData) {
    return this.request('/api/admin/products', {
      method: 'POST',
      body: JSON.stringify(productData)
    });
  },

  updateProduct(id, productData) {
    return this.request(`/api/admin/products/${id}`, {
      method: 'PUT',
      body: JSON.stringify(productData)
    });
  },

  deleteProduct(id) {
    return this.request(`/api/admin/products/${id}`, {
      method: 'DELETE'
    });
  }
};
