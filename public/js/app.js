/**
 * Main Application Orchestrator for SoapSphere Store
 */
const App = {
  currentCategory: 'All',
  searchQuery: '',
  currentSort: 'featured',
  products: [],
  selectedProduct: null,

  async init() {
    console.log("Initializing SoapSphere E-Commerce...");
    Cart.updateBadge();
    await Auth.init();
    await this.loadCategories();
    await this.loadProducts();
    this.setupEventListeners();
  },

  setupEventListeners() {
    // Search input with debounce
    const searchInput = document.getElementById('search-input');
    const clearBtn = document.getElementById('clear-search');
    let debounceTimer;

    searchInput?.addEventListener('input', (e) => {
      clearTimeout(debounceTimer);
      const val = e.target.value.trim();
      if (clearBtn) clearBtn.style.display = val ? 'block' : 'none';

      debounceTimer = setTimeout(() => {
        this.searchQuery = val;
        this.loadProducts();
      }, 300);
    });

    clearBtn?.addEventListener('click', () => {
      if (searchInput) searchInput.value = '';
      clearBtn.style.display = 'none';
      this.searchQuery = '';
      this.loadProducts();
    });

    // Sort dropdown
    document.getElementById('sort-select')?.addEventListener('change', (e) => {
      this.currentSort = e.target.value;
      this.loadProducts();
    });
  },

  async loadCategories() {
    const container = document.getElementById('category-pills');
    if (!container) return;

    try {
      const res = await API.getCategories();
      if (res.success && res.categories) {
        container.innerHTML = res.categories.map(cat => `
          <button class="cat-pill ${cat === this.currentCategory ? 'active' : ''}" 
                  onclick="App.setCategory('${cat}')">
            ${cat}
          </button>
        `).join('');
      }
    } catch (e) {
      console.error("Failed to load categories:", e);
    }
  },

  setCategory(category) {
    this.currentCategory = category;
    document.querySelectorAll('.cat-pill').forEach(btn => {
      btn.classList.toggle('active', btn.textContent.trim() === category);
    });
    this.loadProducts();
  },

  async loadProducts() {
    const grid = document.getElementById('products-grid');
    const countEl = document.getElementById('catalogue-count');
    if (!grid) return;

    grid.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 40px; color: var(--color-slate-400);">
        <div style="display:inline-block; width:24px; height:24px; border:3px solid var(--color-emerald-500); border-radius:50%; border-top-color:transparent; animation:spin 0.8s linear infinite;"></div>
        <p style="margin-top:10px; font-weight:600;">Loading collection...</p>
      </div>
    `;

    try {
      const res = await API.getProducts(this.currentCategory, this.searchQuery, this.currentSort);
      if (!res.success) throw new Error("Could not fetch products");

      this.products = res.products;
      if (countEl) countEl.textContent = `${this.products.length} products found`;

      if (this.products.length === 0) {
        grid.innerHTML = `
          <div class="empty-state" style="grid-column: 1 / -1;">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="1.5">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            <h3>No products found</h3>
            <p>Try adjusting your search terms or category filter.</p>
          </div>
        `;
        return;
      }

      grid.innerHTML = this.products.map(p => `
        <div class="product-card">
          <div class="card-img-wrap" onclick="App.openProductDetail(${p.id})">
            <img src="${p.image_url}" alt="${p.title}" class="card-img" loading="lazy" />
            ${p.is_featured ? '<span class="badge-featured">Featured</span>' : ''}
            <span class="badge-category">${p.category}</span>
          </div>
          <div class="card-body">
            <div class="card-rating">
              <span class="stars">★★★★★</span>
              <span>${p.rating.toFixed(1)} (${p.rating_count || 18})</span>
            </div>
            <h3 class="card-title" onclick="App.openProductDetail(${p.id})">${p.title}</h3>
            <p class="card-desc">${p.description}</p>
            <div class="card-footer">
              <div>
                <div class="card-price">₹${p.price.toLocaleString('en-IN')}</div>
                <div class="card-stock">${p.stock > 0 ? `In Stock (${p.stock})` : '<span style="color:var(--color-red-600)">Out of stock</span>'}</div>
              </div>
              <button class="btn-add-cart" onclick="App.quickAddToCart(${p.id})">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <line x1="12" y1="5" x2="12" y2="19"></line>
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
                <span>Add</span>
              </button>
            </div>
          </div>
        </div>
      `).join('');
    } catch (e) {
      grid.innerHTML = `<div style="grid-column: 1 / -1; text-align: center; color: var(--color-red-600); padding: 40px;">Error loading products: ${e.message}</div>`;
    }
  },

  quickAddToCart(productId) {
    const p = this.products.find(item => item.id === productId);
    if (p) {
      Cart.addItem(p, 1);
    }
  },

  async openProductDetail(productId) {
    try {
      const res = await API.getProduct(productId);
      if (!res.success) return;
      const p = res.product;
      this.selectedProduct = p;

      const modal = document.getElementById('product-detail-modal');
      if (!modal) return;

      document.getElementById('detail-img').src = p.image_url;
      document.getElementById('detail-title').textContent = p.title;
      document.getElementById('detail-category').textContent = p.category;
      document.getElementById('detail-price').textContent = `₹${p.price.toLocaleString('en-IN')}`;
      document.getElementById('detail-desc').textContent = p.description;
      document.getElementById('detail-stock').textContent = p.stock > 0 ? `In Stock (${p.stock} units available)` : 'Out of Stock';
      document.getElementById('detail-qty').value = 1;

      modal.classList.add('open');
    } catch (e) {
      Cart.showToast("Failed to load product details: " + e.message);
    }
  },

  closeProductDetail() {
    document.getElementById('product-detail-modal')?.classList.remove('open');
  },

  addDetailToCart() {
    if (!this.selectedProduct) return;
    const qty = parseInt(document.getElementById('detail-qty').value, 10) || 1;
    Cart.addItem(this.selectedProduct, qty);
    this.closeProductDetail();
  },

  async openOrdersModal() {
    const modal = document.getElementById('orders-modal');
    const tbody = document.getElementById('my-orders-tbody');
    if (!modal || !tbody) return;

    modal.classList.add('open');
    tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; padding:20px;">Fetching your orders...</td></tr>`;

    try {
      const res = await API.getMyOrders();
      if (!res.success) throw new Error(res.error || "Failed to load orders");

      if (res.orders.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; padding:30px; color:var(--color-slate-500);">You have not placed any orders yet.</td></tr>`;
        return;
      }

      tbody.innerHTML = res.orders.map(o => `
        <tr>
          <td><strong style="color:var(--color-black);">${o.order_number}</strong></td>
          <td>${o.created_at.slice(0, 10)}</td>
          <td>
            <div style="font-size:0.8rem;">
              ${o.items.map(it => `<div>• ${it.quantity}x ${it.product_title}</div>`).join('')}
            </div>
          </td>
          <td><strong>₹${o.total_amount.toLocaleString('en-IN')}</strong></td>
          <td>
            <span style="display:inline-block; padding:3px 8px; border-radius:4px; font-weight:700; font-size:0.75rem; text-transform:uppercase; 
              ${o.status === 'paid' ? 'background:#d1fae5; color:#065f46;' : 'background:#f1f5f9; color:#334155;'}">
              ${o.status}
            </span>
          </td>
        </tr>
      `).join('');
    } catch (e) {
      tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; color:var(--color-red-600);">Error: ${e.message}</td></tr>`;
    }
  },

  closeOrdersModal() {
    document.getElementById('orders-modal')?.classList.remove('open');
  }
};

// CSS Spin keyframe
const styleEl = document.createElement('style');
styleEl.textContent = `@keyframes spin { 100% { transform: rotate(360deg); } }`;
document.head.appendChild(styleEl);

// Initialize upon DOM load
document.addEventListener('DOMContentLoaded', () => App.init());
