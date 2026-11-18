/**
 * Cart Manager for VERDANT Store
 * Handles localStorage persistence and UI rendering.
 */
const Cart = {
  storageKey: 'verdant_cart',

  getItems() {
    try {
      const data = localStorage.getItem(this.storageKey);
      return data ? JSON.parse(data) : [];
    } catch (e) {
      console.error("Failed to parse cart storage:", e);
      return [];
    }
  },

  saveItems(items) {
    localStorage.setItem(this.storageKey, JSON.stringify(items));
    this.updateBadge();
    this.renderDrawer();
  },

  addItem(product, quantity = 1) {
    let items = this.getItems();
    const existing = items.find(item => item.product_id === product.id);

    if (existing) {
      existing.quantity += quantity;
    } else {
      items.push({
        product_id: product.id,
        title: product.title,
        price: product.price,
        image_url: product.image_url,
        category: product.category,
        quantity: quantity
      });
    }

    this.saveItems(items);
    this.showToast(`Added "${product.title}" to cart`);
  },

  updateQuantity(productId, delta) {
    let items = this.getItems();
    const item = items.find(i => i.product_id === productId);
    if (!item) return;

    item.quantity += delta;
    if (item.quantity <= 0) {
      items = items.filter(i => i.product_id !== productId);
    }
    this.saveItems(items);
  },

  removeItem(productId) {
    let items = this.getItems();
    items = items.filter(i => i.product_id !== productId);
    this.saveItems(items);
    this.showToast("Item removed from cart");
  },

  clearCart() {
    localStorage.removeItem(this.storageKey);
    this.updateBadge();
    this.renderDrawer();
  },

  getTotals() {
    const items = this.getItems();
    const subtotal = items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    const tax = Math.round(subtotal * 0.18 * 100) / 100;
    const shipping = subtotal >= 499 || subtotal === 0 ? 0 : 49;
    const total = Math.round((subtotal + tax + shipping) * 100) / 100;
    const totalCount = items.reduce((sum, item) => sum + item.quantity, 0);

    return {
      subtotal: subtotal.toFixed(2),
      tax: tax.toFixed(2),
      shipping: shipping === 0 ? "Free" : `₹${shipping}`,
      total: total.toFixed(2),
      count: totalCount
    };
  },

  updateBadge() {
    const totals = this.getTotals();
    const badge = document.getElementById('cart-badge');
    if (badge) {
      badge.textContent = totals.count;
      badge.style.display = totals.count > 0 ? 'flex' : 'none';
    }
  },

  openDrawer() {
    document.getElementById('cart-drawer')?.classList.add('open');
    document.getElementById('cart-overlay')?.classList.add('open');
    this.renderDrawer();
  },

  closeDrawer() {
    document.getElementById('cart-drawer')?.classList.remove('open');
    document.getElementById('cart-overlay')?.classList.remove('open');
  },

  renderDrawer() {
    const container = document.getElementById('cart-items-container');
    const footer = document.getElementById('cart-footer-content');
    if (!container || !footer) return;

    const items = this.getItems();
    const totals = this.getTotals();

    if (items.length === 0) {
      container.innerHTML = `
        <div class="empty-state">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="1.5">
            <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
            <line x1="3" y1="6" x2="21" y2="6"></line>
            <path d="M16 10a4 4 0 0 1-8 0"></path>
          </svg>
          <h3>Your cart is empty</h3>
          <p>Discover our top Flipkart-style deals and add items to your cart.</p>
        </div>
      `;
      footer.style.display = 'none';
      return;
    }

    footer.style.display = 'block';

    container.innerHTML = items.map(item => `
      <div class="cart-item">
        <img src="${item.image_url}" alt="${item.title}" class="cart-item-img" />
        <div class="cart-item-info">
          <div>
            <div class="cart-item-title">${item.title}</div>
            <div class="cart-item-price">₹${(item.price * item.quantity).toLocaleString('en-IN')}</div>
          </div>
          <div class="cart-item-controls">
            <div class="qty-stepper">
              <button class="qty-btn" onclick="Cart.updateQuantity(${item.product_id}, -1)">−</button>
              <span class="qty-count">${item.quantity}</span>
              <button class="qty-btn" onclick="Cart.updateQuantity(${item.product_id}, 1)">+</button>
            </div>
            <button class="remove-item-btn" onclick="Cart.removeItem(${item.product_id})">Remove</button>
          </div>
        </div>
      </div>
    `).join('');

    // Summary lines in INR
    document.getElementById('cart-subtotal').textContent = `₹${parseFloat(totals.subtotal).toLocaleString('en-IN')}`;
    document.getElementById('cart-tax').textContent = `₹${parseFloat(totals.tax).toLocaleString('en-IN')}`;
    document.getElementById('cart-shipping').textContent = totals.shipping;
    document.getElementById('cart-total').textContent = `₹${parseFloat(totals.total).toLocaleString('en-IN')}`;
  },

  showToast(message) {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2.5">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
        <polyline points="22 4 12 14.01 9 11.01"></polyline>
      </svg>
      <span>${message}</span>
    `;
    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      setTimeout(() => toast.remove(), 300);
    }, 2800);
  }
};
