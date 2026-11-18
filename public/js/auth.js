/**
 * Authentication Manager for VERDANT Store
 */
const Auth = {
  currentUser: null,

  async init() {
    const token = API.getToken();
    if (!token) {
      this.updateUI(null);
      return;
    }
    try {
      const res = await API.getMe();
      if (res.success && res.user) {
        this.currentUser = res.user;
        this.updateUI(this.currentUser);
      } else {
        this.logout();
      }
    } catch (e) {
      this.logout();
    }
  },

  updateUI(user) {
    const authContainer = document.getElementById('auth-nav-container');
    const adminBtn = document.getElementById('admin-portal-btn');
    if (!authContainer) return;

    if (user) {
      authContainer.innerHTML = `
        <div style="display: flex; align-items: center; gap: 8px;">
          <button class="btn-secondary" onclick="App.openOrdersModal()" title="View Order History">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="16" y1="13" x2="8" y2="13"></line>
              <line x1="16" y1="17" x2="8" y2="17"></line>
            </svg>
            <span>Orders</span>
          </button>
          <div style="font-size: 0.85rem; font-weight: 700; color: var(--color-black);">
            ${user.name.split(' ')[0]}
          </div>
          <button class="btn-secondary" onclick="Auth.logout()" title="Sign Out" style="padding: 6px 12px;">
            Logout
          </button>
        </div>
      `;
      if (adminBtn) {
        adminBtn.style.display = user.role === 'admin' ? 'inline-flex' : 'none';
      }
    } else {
      authContainer.innerHTML = `
        <button class="btn-secondary" onclick="Auth.openModal('login')">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
          <span>Sign In</span>
        </button>
      `;
      if (adminBtn) adminBtn.style.display = 'none';
    }
  },

  openModal(mode = 'login') {
    const modal = document.getElementById('auth-modal');
    if (!modal) return;
    this.switchTab(mode);
    modal.classList.add('open');
  },

  closeModal() {
    document.getElementById('auth-modal')?.classList.remove('open');
    this.hideError();
  },

  switchTab(tab) {
    const isLogin = tab === 'login';
    document.getElementById('auth-tab-login').classList.toggle('active', isLogin);
    document.getElementById('auth-tab-register').classList.toggle('active', !isLogin);
    document.getElementById('auth-login-fields').style.display = isLogin ? 'block' : 'none';
    document.getElementById('auth-register-fields').style.display = !isLogin ? 'block' : 'none';
    document.getElementById('auth-submit-btn').textContent = isLogin ? 'Sign In to Account' : 'Create Free Account';
    this.hideError();
  },

  fillDemo(type) {
    if (type === 'admin') {
      document.getElementById('login-email').value = 'admin@store.com';
      document.getElementById('login-password').value = 'Admin@123';
      this.switchTab('login');
    } else {
      document.getElementById('login-email').value = 'user@store.com';
      document.getElementById('login-password').value = 'User@123';
      this.switchTab('login');
    }
  },

  async handleSubmit(e) {
    e.preventDefault();
    this.hideError();
    const isLogin = document.getElementById('auth-tab-login').classList.contains('active');

    try {
      let res;
      if (isLogin) {
        const email = document.getElementById('login-email').value.trim();
        const password = document.getElementById('login-password').value;
        res = await API.login(email, password);
      } else {
        const name = document.getElementById('reg-name').value.trim();
        const email = document.getElementById('reg-email').value.trim();
        const password = document.getElementById('reg-password').value;
        res = await API.register(name, email, password);
      }

      if (res.success && res.token) {
        localStorage.setItem('verdant_token', res.token);
        this.currentUser = res.user;
        this.updateUI(this.currentUser);
        this.closeModal();
        Cart.showToast(`Welcome back, ${res.user.name}!`);
      }
    } catch (err) {
      this.showError(err.message || "Authentication failed");
    }
  },

  showError(msg) {
    const el = document.getElementById('auth-error-banner');
    if (el) {
      el.textContent = msg;
      el.style.display = 'block';
    }
  },

  hideError() {
    const el = document.getElementById('auth-error-banner');
    if (el) el.style.display = 'none';
  },

  logout() {
    localStorage.removeItem('verdant_token');
    this.currentUser = null;
    this.updateUI(null);
    Cart.showToast("Signed out successfully");
  }
};
