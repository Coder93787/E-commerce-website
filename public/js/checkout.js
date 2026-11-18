/**
 * Checkout & Payment Gateway Manager
 * Simulates Stripe & Razorpay test mode payment processing.
 * Strictly guarantees orders are created ONLY after payment succeeds.
 */
const Checkout = {
  currentGateway: 'stripe',
  isProcessing: false,

  openModal() {
    const items = Cart.getItems();
    if (items.length === 0) {
      Cart.showToast("Your cart is empty!");
      return;
    }

    Cart.closeDrawer();
    const modal = document.getElementById('checkout-modal');
    if (!modal) return;

    // Reset view to form step
    document.getElementById('checkout-form-step').style.display = 'block';
    document.getElementById('checkout-success-step').style.display = 'none';
    this.hideError();

    // Auto-fill user information if logged in
    if (Auth.currentUser) {
      document.getElementById('checkout-name').value = Auth.currentUser.name || '';
      document.getElementById('checkout-email').value = Auth.currentUser.email || '';
    }

    // Default test card info
    this.fillCard('success');
    this.updatePayButton();
    modal.classList.add('open');
  },

  closeModal() {
    if (this.isProcessing) return; // Prevent closing mid-transaction
    document.getElementById('checkout-modal')?.classList.remove('open');
  },

  setGateway(gateway) {
    this.currentGateway = gateway;
    document.getElementById('tab-stripe').classList.toggle('active', gateway === 'stripe');
    document.getElementById('tab-razorpay').classList.toggle('active', gateway === 'razorpay');
    
    const isRzp = gateway === 'razorpay';
    document.getElementById('gateway-badge-text').textContent = isRzp 
      ? 'Razorpay Test Mode (Simulated Gateway)' 
      : 'Stripe Test Mode (Simulated Gateway)';
  },

  fillCard(type) {
    if (type === 'success') {
      document.getElementById('card-number').value = '4242 4242 4242 4242';
      document.getElementById('card-expiry').value = '12/28';
      document.getElementById('card-cvv').value = '345';
      document.getElementById('card-name').value = document.getElementById('checkout-name').value || 'Jane Doe';
      this.hideError();
    } else {
      // 4000 0000 0000 0002 is Stripe's standard test declined card number
      document.getElementById('card-number').value = '4000 0000 0000 0002';
      document.getElementById('card-expiry').value = '08/27';
      document.getElementById('card-cvv').value = '999';
      document.getElementById('card-name').value = 'Declined Test Card';
      this.hideError();
    }
  },

  updatePayButton() {
    const totals = Cart.getTotals();
    const btn = document.getElementById('pay-submit-btn');
    if (btn) {
      btn.innerHTML = `
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
          <line x1="1" y1="10" x2="23" y2="10"></line>
        </svg>
        <span>Authorize & Pay ₹${parseFloat(totals.total).toLocaleString('en-IN')}</span>
      `;
    }
  },

  async handlePayment(e) {
    e.preventDefault();
    if (this.isProcessing) return;

    this.hideError();
    const name = document.getElementById('checkout-name').value.trim();
    const email = document.getElementById('checkout-email').value.trim();
    const address = document.getElementById('checkout-address').value.trim();
    const cardNumber = document.getElementById('card-number').value.replace(/\s+/g, '');
    const expiry = document.getElementById('card-expiry').value.trim();
    const cvv = document.getElementById('card-cvv').value.trim();

    if (!name || !email || !address) {
      this.showError("Please enter your name, email, and shipping address.");
      return;
    }

    if (cardNumber.length < 13 || !expiry || !cvv) {
      this.showError("Please enter complete card payment details.");
      return;
    }

    const cartItems = Cart.getItems();
    if (cartItems.length === 0) {
      this.showError("Your cart is empty.");
      return;
    }

    // Set loading state
    this.isProcessing = true;
    const btn = document.getElementById('pay-submit-btn');
    btn.disabled = true;
    btn.innerHTML = `
      <div style="display:inline-block; width:16px; height:16px; border:2px solid #ffffff; border-radius:50%; border-top-color:transparent; animation:spin 0.6s linear infinite; margin-right:8px;"></div>
      <span>Connecting to ${this.currentGateway === 'stripe' ? 'Stripe' : 'Razorpay'}...</span>
    `;

    const payload = {
      gateway: this.currentGateway,
      customer_name: name,
      customer_email: email,
      shipping_address: address,
      cart_items: cartItems,
      payment_info: {
        card_number: cardNumber,
        expiry: expiry,
        cvv: cvv
      }
    };

    try {
      // Simulate real-world 1-second gateway handshake latency
      await new Promise(r => setTimeout(r, 900));

      const res = await API.processPayment(payload);

      if (res.success && res.order) {
        // Payment Succeeded!
        Cart.clearCart(); // Cart cleared only upon confirmed order creation
        this.renderSuccess(res.order, res.payment_id);
      } else {
        throw new Error(res.error || "Payment transaction failed.");
      }
    } catch (err) {
      console.warn("Payment error caught:", err);
      this.showError(err.message || "Payment declined. Cart preserved so you can retry.");
      btn.disabled = false;
      this.updatePayButton();
    } finally {
      this.isProcessing = false;
    }
  },

  renderSuccess(order, paymentId) {
    document.getElementById('checkout-form-step').style.display = 'none';
    const successStep = document.getElementById('checkout-success-step');
    successStep.style.display = 'block';

    document.getElementById('success-order-num').textContent = order.order_number;
    document.getElementById('success-payment-id').textContent = paymentId;
    document.getElementById('success-total-paid').textContent = `₹${parseFloat(order.total_amount).toLocaleString('en-IN')}`;
    document.getElementById('success-items-count').textContent = `${order.items.reduce((s, i) => s + i.quantity, 0)} items`;

    Cart.showToast("Payment verified! Order placed successfully.");
  },

  showError(msg) {
    const el = document.getElementById('checkout-error-banner');
    if (el) {
      el.textContent = msg;
      el.style.display = 'block';
    }
  },

  hideError() {
    const el = document.getElementById('checkout-error-banner');
    if (el) el.style.display = 'none';
  }
};
