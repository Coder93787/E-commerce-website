"""
Database Layer for E-Commerce Store
Handles SQLite tables, migrations, password hashing, and ACID transactions.
"""
import sqlite3
import hashlib
import secrets
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'store.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    if not salt:
        salt = secrets.token_hex(16)
    pw_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100_000
    ).hex()
    return pw_hash, salt

def verify_password(password: str, salt: str, expected_hash: str) -> bool:
    pw_hash, _ = hash_password(password, salt)
    return secrets.compare_digest(pw_hash, expected_hash)

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        
        # 1. Users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL COLLATE NOCASE,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'customer',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # 2. Sessions table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """)

        # 3. Products table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            category TEXT NOT NULL,
            image_url TEXT NOT NULL,
            stock INTEGER NOT NULL DEFAULT 10,
            rating REAL DEFAULT 4.8,
            rating_count INTEGER DEFAULT 25,
            is_featured INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # 4. Orders table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT UNIQUE NOT NULL,
            user_id INTEGER,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            shipping_address TEXT NOT NULL,
            subtotal REAL NOT NULL,
            tax REAL NOT NULL,
            total_amount REAL NOT NULL,
            payment_gateway TEXT NOT NULL,
            payment_id TEXT,
            status TEXT NOT NULL DEFAULT 'paid',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
        )
        """)

        # 5. Order items
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER,
            product_title TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL
        )
        """)

        # 6. Payment logs
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS payment_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_ref TEXT UNIQUE NOT NULL,
            user_id INTEGER,
            gateway TEXT NOT NULL,
            amount REAL NOT NULL,
            currency TEXT DEFAULT 'INR',
            status TEXT NOT NULL,
            card_last4 TEXT,
            error_message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()

# --- Auth Helpers ---

def create_user(name: str, email: str, password: str, role: str = 'customer'):
    pw_hash, salt = hash_password(password)
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password_hash, salt, role) VALUES (?, ?, ?, ?, ?)",
            (name.strip(), email.strip().lower(), pw_hash, salt, role)
        )
        conn.commit()
        return cursor.lastrowid

def authenticate_user(email: str, password: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email.strip().lower(),))
        user = cursor.fetchone()
        if not user:
            return None
        if verify_password(password, user['salt'], user['password_hash']):
            token = secrets.token_hex(32)
            expires_at = datetime.utcnow() + timedelta(days=7)
            cursor.execute(
                "INSERT INTO sessions (token, user_id, expires_at) VALUES (?, ?, ?)",
                (token, user['id'], expires_at.isoformat())
            )
            conn.commit()
            return {
                "token": token,
                "user": {
                    "id": user['id'],
                    "name": user['name'],
                    "email": user['email'],
                    "role": user['role']
                }
            }
        return None

def get_user_by_token(token: str):
    if not token:
        return None
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.id, u.name, u.email, u.role, s.expires_at 
            FROM sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.token = ?
        """, (token,))
        row = cursor.fetchone()
        if not row:
            return None
        expires_at = datetime.fromisoformat(row['expires_at'])
        if datetime.utcnow() > expires_at:
            cursor.execute("DELETE FROM sessions WHERE token = ?", (token,))
            conn.commit()
            return None
        return {
            "id": row['id'],
            "name": row['name'],
            "email": row['email'],
            "role": row['role']
        }

def logout_user(token: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sessions WHERE token = ?", (token,))
        conn.commit()

# --- Product Helpers ---

def get_products(category=None, search=None, sort_by=None):
    with get_db() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM products WHERE 1=1"
        params = []
        
        if category and category.lower() != 'all':
            query += " AND LOWER(category) = ?"
            params.append(category.lower())
            
        if search:
            query += " AND (LOWER(title) LIKE ? OR LOWER(description) LIKE ?)"
            term = f"%{search.lower()}%"
            params.extend([term, term])
            
        if sort_by == 'price_asc':
            query += " ORDER BY price ASC"
        elif sort_by == 'price_desc':
            query += " ORDER BY price DESC"
        elif sort_by == 'rating':
            query += " ORDER BY rating DESC"
        elif sort_by == 'newest':
            query += " ORDER BY id DESC"
        else:
            query += " ORDER BY is_featured DESC, id DESC"
            
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(r) for r in rows]

def get_product(product_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_categories():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM products ORDER BY category")
        rows = cursor.fetchall()
        return [r['category'] for r in rows]

# --- Admin Helpers ---

def add_product(data: dict):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO products (title, description, price, category, image_url, stock, rating, is_featured)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['title'].strip(),
            data.get('description', '').strip(),
            float(data['price']),
            data['category'].strip(),
            data.get('image_url', '').strip(),
            int(data.get('stock', 10)),
            float(data.get('rating', 4.8)),
            int(data.get('is_featured', 0))
        ))
        conn.commit()
        return cursor.lastrowid

def update_product(product_id: int, data: dict):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE products
            SET title = ?, description = ?, price = ?, category = ?, image_url = ?, stock = ?, is_featured = ?
            WHERE id = ?
        """, (
            data['title'].strip(),
            data.get('description', '').strip(),
            float(data['price']),
            data['category'].strip(),
            data.get('image_url', '').strip(),
            int(data.get('stock', 0)),
            int(data.get('is_featured', 0)),
            product_id
        ))
        conn.commit()
        return cursor.rowcount > 0

def delete_product(product_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        return cursor.rowcount > 0

# --- Payment & Order Helpers ---

def record_payment_log(tx_ref: str, user_id: int, gateway: str, amount: float, status: str, card_last4: str = None, error_message: str = None):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO payment_logs (transaction_ref, user_id, gateway, amount, status, card_last4, error_message)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (tx_ref, user_id, gateway, amount, status, card_last4, error_message))
        conn.commit()
        return cursor.lastrowid

def create_order_after_payment(user_id: int, customer_name: str, customer_email: str, shipping_address: str, cart_items: list, gateway: str, payment_id: str):
    with get_db() as conn:
        cursor = conn.cursor()
        
        subtotal = 0.0
        verified_items = []
        for item in cart_items:
            p_id = item['product_id']
            qty = int(item['quantity'])
            if qty <= 0:
                continue
            cursor.execute("SELECT id, title, price, stock FROM products WHERE id = ?", (p_id,))
            p = cursor.fetchone()
            if not p:
                raise ValueError(f"Product with ID {p_id} not found.")
            if p['stock'] < qty:
                raise ValueError(f"Insufficient stock for '{p['title']}'. Only {p['stock']} remaining.")
            
            item_total = p['price'] * qty
            subtotal += item_total
            verified_items.append({
                'product_id': p['id'],
                'title': p['title'],
                'price': p['price'],
                'quantity': qty
            })
            
        if not verified_items:
            raise ValueError("Cart is empty.")
            
        tax = round(subtotal * 0.18, 2)
        total_amount = round(subtotal + tax, 2)
        
        order_number = f"ORD-{secrets.token_hex(4).upper()}-{int(datetime.utcnow().timestamp()) % 10000:04d}"
        
        cursor.execute("""
            INSERT INTO orders (order_number, user_id, customer_name, customer_email, shipping_address, subtotal, tax, total_amount, payment_gateway, payment_id, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'paid')
        """, (order_number, user_id, customer_name, customer_email, shipping_address, subtotal, tax, total_amount, gateway, payment_id))
        
        order_id = cursor.lastrowid
        
        for v in verified_items:
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, product_title, quantity, unit_price)
                VALUES (?, ?, ?, ?, ?)
            """, (order_id, v['product_id'], v['title'], v['quantity'], v['price']))
            
            cursor.execute("""
                UPDATE products SET stock = stock - ? WHERE id = ?
            """, (v['quantity'], v['product_id']))
            
        conn.commit()
        return {
            "order_id": order_id,
            "order_number": order_number,
            "total_amount": total_amount,
            "subtotal": subtotal,
            "tax": tax,
            "status": "paid",
            "items": verified_items
        }

def get_user_orders(user_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE user_id = ? ORDER BY id DESC", (user_id,))
        orders = [dict(r) for r in cursor.fetchall()]
        for o in orders:
            cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (o['id'],))
            o['items'] = [dict(it) for it in cursor.fetchall()]
        return orders

def get_all_orders():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders ORDER BY id DESC")
        orders = [dict(r) for r in cursor.fetchall()]
        for o in orders:
            cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (o['id'],))
            o['items'] = [dict(it) for it in cursor.fetchall()]
        return orders

def update_order_status(order_id: int, new_status: str):
    valid_statuses = ['paid', 'processing', 'shipped', 'delivered', 'cancelled']
    if new_status not in valid_statuses:
        raise ValueError(f"Invalid status. Choose from {valid_statuses}")
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
        conn.commit()
        return cursor.rowcount > 0

def get_admin_metrics():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as total_products, SUM(stock) as total_inventory FROM products")
        prod_row = cursor.fetchone()
        
        cursor.execute("SELECT COUNT(*) as total_orders, COALESCE(SUM(total_amount), 0) as total_revenue FROM orders WHERE status != 'cancelled'")
        order_row = cursor.fetchone()
        
        cursor.execute("SELECT COUNT(*) as total_users FROM users WHERE role = 'customer'")
        user_row = cursor.fetchone()
        
        return {
            "total_products": prod_row['total_products'] or 0,
            "total_inventory": prod_row['total_inventory'] or 0,
            "total_orders": order_row['total_orders'] or 0,
            "total_revenue": round(order_row['total_revenue'] or 0.0, 2),
            "total_users": user_row['total_users'] or 0
        }
