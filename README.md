# SoapSphere — Full-Stack E-Commerce Store

A high-contrast, modern full-stack E-Commerce platform built in **Pure White, Emerald Green, and Obsidian Black**.

Designed according to **Track A (Days 1-15): Full-Stack Product**:
- ✅ **Product Catalogue**: Categories, real-time live search, price & rating sorting.
- ✅ **Product Details View**: Image previews, specs, stock quantity indicators, add-to-cart.
- ✅ **Persistent Cart**: Saved in browser `localStorage`, survives page reloads seamlessly.
- ✅ **Order Placement & History**: Customer order tracking with line items and delivery status.
- ✅ **Admin Panel**: Dashboard metrics (Revenue, Inventory, Orders), Product CRUD, and Order status management.
- ✅ **User Authentication**: Secure signup/login with PBKDF2-HMAC-SHA256 password hashing.
- ✅ **Heavy Feature (Payment Gateway Integration)**: Interactive test-mode payments (Stripe & Razorpay simulation). Orders are created **only after payment succeeds**, and card declines/failures are cleanly handled with the cart preserved.

---

## Quickstart

### 1. Launch the Server
```bash
cd /Users/mdshahidafridi/.gemini/antigravity/scratch/ecommerce-store
python3 server.py
```

### 2. Open in Browser
Visit:
```
http://127.0.0.1:8000
```

---

## Pre-Configured Accounts

| Role | Email | Password | Features Accessible |
| :--- | :--- | :--- | :--- |
| **Store Admin** | `admin@store.com` | `Admin@123` | Full Admin Hub, Add/Edit/Delete Products, Manage Orders & Revenue |
| **Demo Customer** | `user@store.com` | `User@123` | Browse, Cart, Checkout, View Personal Order History |

*(You can also use the one-click demo login buttons in the Sign-In modal!)*

---

## Testing the Heavy Feature: Payment Gateway Simulation

When you proceed to checkout, you will see the **Interactive Test Mode**:
1. **Successful Payment Flow**:
   - Click the green **"Auto-Fill: Card Success (4242...)"** chip.
   - Click **"Authorize & Pay"**.
   - The gateway approves the payment, stock is deducted in SQLite, the order is created, receipt is displayed, and cart is cleared.
2. **Declined Payment Flow**:
   - Click the red **"Auto-Fill: Card Decline (0002...)"** chip.
   - Click **"Authorize & Pay"**.
   - The bank declines the transaction: an error alert appears, **no order is generated**, and **your cart remains intact** so you can retry.

---

## Architecture

- **Backend**: Python standard library HTTP server (`http.server`) & SQLite3 database (`store.db`). Zero external packages required.
- **Frontend**: Component-driven SPA in HTML5, CSS3 (Custom design system in Obsidian Black, Emerald Green, and Pure White), and Vanilla JavaScript modules.
