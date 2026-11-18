/**
 * Admin Panel Manager for VERDANT Store
 * Handles product catalog CRUD and customer order updates.
 */
const Admin = {
  currentTab: 'products',

  async openModal() {
    if (!Auth.currentUser || Auth.currentUser.role !== 'admin') {
      Cart.showToast("Admin privileges required.");
      return;
    }
    const modal = document.getElementById('admin-modal');
    if (!modal) return;
    modal.classList.add('open');
    this.switchTab('products');
    await this.loadMetrics();
  },

  closeModal() {
    document.getElementById('admin-modal')?.classList.remove('open');
  },

  switchTab(tab) {
    this.currentTab = tab;
    document.getElementById('admin-tab-products').classList.toggle('active', tab === 'products');
    document.getElementById('admin-tab-orders').classList.toggle('active', tab === 'orders');
    
    document.getElementById('admin-products-view').style.display = tab === 'products' ? 'block' : 'none';
    document.getElementById('admin-orders-view').style.display = tab === 'orders' ? 'block' : 'none';

    if (tab === 'products') {
      this.loadProducts();
    } else {
      this.loadOrders();
    }
  },

  async loadMetrics() {
    try {
      const res = await API.getAdminMetrics();
      if (res.success && res.metrics) {
        const m = res.metrics;
        document.getElementById('metric-products').textContent = m.total_products;
        document.getElementById('metric-inventory').textContent = m.total_inventory;
        document.getElementById('metric-orders').textContent = m.total_orders;
        document.getElementById('metric-revenue').textContent = `₹${parseFloat(m.total_revenue).toLocaleString('en-IN')}`;
      }
    } catch (e) {
      console.error("Failed to load metrics:", e);
    }
  },

  async loadProducts() {
    const tbody = document.getElementById('admin-products-tbody');
    if (!tbody) return;
    tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding:20px;">Loading inventory...</td></tr>`;

    try {
      const res = await API.getProducts();
      if (!res.success) throw new Error("Failed to load products");

      tbody.innerHTML = res.products.map(p => `
        <tr>
          <td>
            <div style="display:flex; align-items:center; gap:10px;">
              <img src="${p.image_url}" alt="" style="width:36px; height:36px; border-radius:4px; object-fit:cover;" />
              <div>
                <strong style="color:var(--color-dark);">${p.title}</strong>
                <div style="font-size:0.75rem; color:var(--color-slate-500);">${p.category}</div>
              </div>
            </div>
          </td>
          <td><strong>₹${p.price.toLocaleString('en-IN')}</strong></td>
          <td>
            <span style="font-weight:700; color:${p.stock < 5 ? 'var(--color-red-600)' : 'var(--color-emerald-700)'};">
              ${p.stock} units
            </span>
          </td>
          <td>${p.is_featured ? '<span style="color:#10b981; font-weight:700;">★ Featured</span>' : 'Standard'}</td>
          <td>
            <div style="display:flex; gap:6px;">
              <button class="btn-secondary" style="padding:4px 8px; font-size:0.75rem;" onclick="Admin.openEditProductModal(${p.id})">Edit</button>
              <button class="btn-secondary" style="padding:4px 8px; font-size:0.75rem; color:var(--color-red-600);" onclick="Admin.deleteProduct(${p.id})">Delete</button>
            </div>
          </td>
        </tr>
      `).join('');
    } catch (e) {
      tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; color:var(--color-red-600);">Error: ${e.message}</td></tr>`;
    }
  },

  async loadOrders() {
    const tbody = document.getElementById('admin-orders-tbody');
    if (!tbody) return;
    tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding:20px;">Loading orders...</td></tr>`;

    try {
      const res = await API.getAdminOrders();
      if (!res.success) throw new Error("Failed to load orders");

      if (res.orders.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding:20px; color:var(--color-slate-500);">No orders found.</td></tr>`;
        return;
      }

      tbody.innerHTML = res.orders.map(o => `
        <tr>
          <td><strong style="color:var(--color-black);">${o.order_number}</strong></td>
          <td>
            <div>${o.customer_name}</div>
            <div style="font-size:0.75rem; color:var(--color-slate-500);">${o.customer_email}</div>
          </td>
          <td>
            <span style="font-size:0.75rem; text-transform:uppercase; font-weight:700; background:var(--color-slate-100); padding:2px 6px; border-radius:4px;">
              ${o.payment_gateway}
            </span>
          </td>
          <td><strong>₹${parseFloat(o.total_amount).toLocaleString('en-IN')}</strong></td>
          <td>
            <select class="status-select" onchange="Admin.updateOrderStatus(${o.id}, this.value)">
              <option value="paid" ${o.status === 'paid' ? 'selected' : ''}>Paid</option>
              <option value="processing" ${o.status === 'processing' ? 'selected' : ''}>Processing</option>
              <option value="shipped" ${o.status === 'shipped' ? 'selected' : ''}>Shipped</option>
              <option value="delivered" ${o.status === 'delivered' ? 'selected' : ''}>Delivered</option>
              <option value="cancelled" ${o.status === 'cancelled' ? 'selected' : ''}>Cancelled</option>
            </select>
          </td>
          <td style="font-size:0.78rem; color:var(--color-slate-500);">${o.created_at.slice(0, 16)}</td>
        </tr>
      `).join('');
    } catch (e) {
      tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; color:var(--color-red-600);">Error: ${e.message}</td></tr>`;
    }
  },

  async updateOrderStatus(orderId, newStatus) {
    try {
      const res = await API.updateOrderStatus(orderId, newStatus);
      if (res.success) {
        Cart.showToast(res.message);
        this.loadMetrics();
      }
    } catch (e) {
      Cart.showToast("Failed to update status: " + e.message);
    }
  },

  openAddProductModal() {
    document.getElementById('edit-product-id').value = '';
    document.getElementById('product-form-title').textContent = 'Add New Product';
    document.getElementById('admin-prod-form').reset();
    document.getElementById('product-editor-modal')?.classList.add('open');
  },

  async openEditProductModal(productId) {
    try {
      const res = await API.getProduct(productId);
      if (!res.success) return;
      const p = res.product;
      document.getElementById('edit-product-id').value = p.id;
      document.getElementById('product-form-title').textContent = `Edit Product: ${p.title}`;
      document.getElementById('prod-input-title').value = p.title;
      document.getElementById('prod-input-category').value = p.category;
      document.getElementById('prod-input-price').value = p.price;
      document.getElementById('prod-input-stock').value = p.stock;
      document.getElementById('prod-input-image').value = p.image_url;
      document.getElementById('prod-input-desc').value = p.description;
      document.getElementById('prod-input-featured').checked = p.is_featured === 1;

      document.getElementById('product-editor-modal')?.classList.add('open');
    } catch (e) {
      Cart.showToast("Failed to fetch product details: " + e.message);
    }
  },

  closeProductEditorModal() {
    document.getElementById('product-editor-modal')?.classList.remove('open');
  },

  async handleProductSubmit(e) {
    e.preventDefault();
    const id = document.getElementById('edit-product-id').value;
    const payload = {
      title: document.getElementById('prod-input-title').value.trim(),
      category: document.getElementById('prod-input-category').value.trim(),
      price: parseFloat(document.getElementById('prod-input-price').value),
      stock: parseInt(document.getElementById('prod-input-stock').value, 10),
      image_url: document.getElementById('prod-input-image').value.trim(),
      description: document.getElementById('prod-input-desc').value.trim(),
      is_featured: document.getElementById('prod-input-featured').checked ? 1 : 0
    };

    try {
      if (id) {
        await API.updateProduct(id, payload);
        Cart.showToast("Product updated successfully!");
      } else {
        await API.createProduct(payload);
        Cart.showToast("Product created successfully!");
      }
      this.closeProductEditorModal();
      this.loadProducts();
      this.loadMetrics();
      App.loadProducts(); // refresh main storefront
    } catch (e) {
      Cart.showToast("Save failed: " + e.message);
    }
  },

  async deleteProduct(productId) {
    if (!confirm("Are you sure you want to delete this product?")) return;
    try {
      await API.deleteProduct(productId);
      Cart.showToast("Product deleted.");
      this.loadProducts();
      this.loadMetrics();
      App.loadProducts();
    } catch (e) {
      Cart.showToast("Delete failed: " + e.message);
    }
  }
};
