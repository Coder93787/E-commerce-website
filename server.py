"""
REST API HTTP Server for E-Commerce Store.
Implements API endpoints, static file serving, test payments, and admin operations.
Zero external dependencies, running on Python standard library.
"""
import http.server
import socketserver
import json
import urllib.parse
import os
import mimetypes
import secrets
from datetime import datetime

import database as db

PORT = int(os.environ.get("PORT", 8000))
PUBLIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'public')

class StoreRequestHandler(http.server.BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        # Clean custom logger
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {self.command} {self.path} - {args[0]}")

    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_cors_headers()
        self.end_headers()

    def send_json(self, data, status=200):
        body = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def send_error_json(self, message, status=400):
        self.send_json({"success": False, "error": message}, status=status)

    def get_auth_user(self):
        auth_header = self.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()
            return db.get_user_by_token(token)
        return None

    def read_json_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            return {}
        raw = self.rfile.read(content_length).decode('utf-8')
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return None

    # --- GET Requests ---
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip('/')
        query = urllib.parse.parse_qs(parsed.query)

        # 1. API: Auth Me
        if path == "/api/auth/me":
            user = self.get_auth_user()
            if not user:
                return self.send_error_json("Unauthorized. Please log in.", 401)
            return self.send_json({"success": True, "user": user})

        # 2. API: Products Catalogue
        elif path == "/api/products":
            category = query.get('category', [None])[0]
            search = query.get('search', [None])[0]
            sort_by = query.get('sort', [None])[0]
            products = db.get_products(category=category, search=search, sort_by=sort_by)
            return self.send_json({"success": True, "count": len(products), "products": products})

        # 3. API: Single Product
        elif path.startswith("/api/products/"):
            try:
                prod_id = int(path.split('/')[-1])
                product = db.get_product(prod_id)
                if not product:
                    return self.send_error_json("Product not found", 404)
                return self.send_json({"success": True, "product": product})
            except ValueError:
                return self.send_error_json("Invalid product ID", 400)

        # 4. API: Categories List
        elif path == "/api/categories":
            cats = db.get_categories()
            return self.send_json({"success": True, "categories": ["All"] + cats})

        # 5. API: Customer's Orders
        elif path == "/api/orders/my-orders":
            user = self.get_auth_user()
            if not user:
                return self.send_error_json("Login required to view order history", 401)
            orders = db.get_user_orders(user['id'])
            return self.send_json({"success": True, "orders": orders})

        # 6. API: Admin Metrics & All Orders
        elif path == "/api/admin/metrics":
            user = self.get_auth_user()
            if not user or user.get('role') != 'admin':
                return self.send_error_json("Forbidden: Admin access required", 403)
            metrics = db.get_admin_metrics()
            return self.send_json({"success": True, "metrics": metrics})

        elif path == "/api/admin/orders":
            user = self.get_auth_user()
            if not user or user.get('role') != 'admin':
                return self.send_error_json("Forbidden: Admin access required", 403)
            orders = db.get_all_orders()
            return self.send_json({"success": True, "orders": orders})

        # 7. Static Files Serving
        else:
            self.serve_static_file(parsed.path)

    # --- POST Requests ---
    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip('/')
        data = self.read_json_body()

        if data is None:
            return self.send_error_json("Invalid JSON body", 400)

        # 1. API: Register
        if path == "/api/auth/register":
            name = data.get("name", "").strip()
            email = data.get("email", "").strip()
            password = data.get("password", "")
            
            if not name or not email or not password:
                return self.send_error_json("Name, email and password are required")
            if len(password) < 6:
                return self.send_error_json("Password must be at least 6 characters")
            
            try:
                user_id = db.create_user(name, email, password, role='customer')
                auth_info = db.authenticate_user(email, password)
                return self.send_json({
                    "success": True,
                    "message": "Account created successfully",
                    "token": auth_info["token"],
                    "user": auth_info["user"]
                }, status=201)
            except Exception as e:
                if "UNIQUE constraint failed" in str(e):
                    return self.send_error_json("Email is already registered")
                return self.send_error_json(f"Registration failed: {str(e)}")

        # 2. API: Login
        elif path == "/api/auth/login":
            email = data.get("email", "").strip()
            password = data.get("password", "")
            if not email or not password:
                return self.send_error_json("Email and password are required")
            
            auth_info = db.authenticate_user(email, password)
            if not auth_info:
                return self.send_error_json("Invalid email or password", 401)
            return self.send_json({
                "success": True,
                "message": "Logged in successfully",
                "token": auth_info["token"],
                "user": auth_info["user"]
            })

        # 3. API: Logout
        elif path == "/api/auth/logout":
            auth_header = self.headers.get("Authorization", "")
            if auth_header.startswith("Bearer "):
                db.logout_user(auth_header[7:].strip())
            return self.send_json({"success": True, "message": "Logged out"})

        # 4. API: Process Payment & Create Order (Heavy Feature)
        elif path == "/api/payments/process":
            user = self.get_auth_user()
            user_id = user['id'] if user else None
            
            gateway = data.get("gateway", "stripe").lower()
            test_action = data.get("test_action", "success")  # "success" or "fail"
            customer_name = data.get("customer_name", "").strip()
            customer_email = data.get("customer_email", "").strip()
            shipping_address = data.get("shipping_address", "").strip()
            cart_items = data.get("cart_items", [])
            payment_info = data.get("payment_info", {})
            
            card_number = str(payment_info.get("card_number", "")).replace(" ", "")
            card_last4 = card_number[-4:] if len(card_number) >= 4 else "4242"
            
            if not customer_name or not customer_email or not shipping_address:
                return self.send_error_json("Customer name, email and shipping address are required")
            if not cart_items:
                return self.send_error_json("Cannot checkout with an empty cart")

            # Check if payment should fail:
            # - user selected "Simulate Decline/Failure" button
            # - or card number ends in 0002 / 0000
            is_failure = (
                test_action == "fail" or
                card_number.endswith("0002") or
                card_number.endswith("0000") or
                payment_info.get("force_decline", False)
            )

            tx_ref = f"{'ch_test_' if gateway == 'stripe' else 'pay_test_'}{secrets.token_hex(8)}"
            
            # Calculate rough amount for logging
            approx_amount = sum(float(item.get('price', 0)) * int(item.get('quantity', 1)) for item in cart_items)

            if is_failure:
                error_msg = "Card declined: Your bank declined the transaction (Test Mode simulation)."
                db.record_payment_log(
                    tx_ref=tx_ref,
                    user_id=user_id,
                    gateway=gateway,
                    amount=approx_amount,
                    status="failed",
                    card_last4=card_last4,
                    error_message=error_msg
                )
                # CRITICAL: Do NOT create order when payment fails!
                return self.send_json({
                    "success": False,
                    "error": error_msg,
                    "gateway": gateway,
                    "transaction_ref": tx_ref,
                    "can_retry": True
                }, status=402) # 402 Payment Required

            # Payment succeeded!
            try:
                order_result = db.create_order_after_payment(
                    user_id=user_id,
                    customer_name=customer_name,
                    customer_email=customer_email,
                    shipping_address=shipping_address,
                    cart_items=cart_items,
                    gateway=gateway,
                    payment_id=tx_ref
                )
                
                db.record_payment_log(
                    tx_ref=tx_ref,
                    user_id=user_id,
                    gateway=gateway,
                    amount=order_result['total_amount'],
                    status="succeeded",
                    card_last4=card_last4
                )

                return self.send_json({
                    "success": True,
                    "message": "Payment verified and order placed successfully!",
                    "payment_id": tx_ref,
                    "order": order_result
                })
            except ValueError as val_err:
                return self.send_error_json(str(val_err), status=400)
            except Exception as e:
                return self.send_error_json(f"Order placement failed: {str(e)}", status=500)

        # 5. API: Admin Add Product
        elif path == "/api/admin/products":
            user = self.get_auth_user()
            if not user or user.get('role') != 'admin':
                return self.send_error_json("Forbidden: Admin access required", 403)
            
            try:
                new_id = db.add_product(data)
                return self.send_json({
                    "success": True,
                    "message": "Product created successfully",
                    "product_id": new_id
                }, status=201)
            except Exception as e:
                return self.send_error_json(f"Failed to add product: {str(e)}")

        else:
            self.send_error_json(f"Endpoint not found: POST {path}", 404)

    # --- PUT Requests ---
    def do_PUT(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip('/')
        data = self.read_json_body()

        # Admin Edit Product
        if path.startswith("/api/admin/products/"):
            user = self.get_auth_user()
            if not user or user.get('role') != 'admin':
                return self.send_error_json("Forbidden: Admin access required", 403)
            try:
                prod_id = int(path.split('/')[-1])
                updated = db.update_product(prod_id, data)
                if not updated:
                    return self.send_error_json("Product not found or not modified", 404)
                return self.send_json({"success": True, "message": "Product updated successfully"})
            except Exception as e:
                return self.send_error_json(f"Update failed: {str(e)}")

        # Admin Update Order Status
        elif path.startswith("/api/admin/orders/") and path.endswith("/status"):
            user = self.get_auth_user()
            if not user or user.get('role') != 'admin':
                return self.send_error_json("Forbidden: Admin access required", 403)
            try:
                parts = path.split('/')
                order_id = int(parts[4])
                status = data.get("status")
                updated = db.update_order_status(order_id, status)
                if not updated:
                    return self.send_error_json("Order not found", 404)
                return self.send_json({"success": True, "message": f"Order status updated to {status}"})
            except Exception as e:
                return self.send_error_json(str(e))

        else:
            self.send_error_json(f"Endpoint not found: PUT {path}", 404)

    # --- DELETE Requests ---
    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip('/')

        # Admin Delete Product
        if path.startswith("/api/admin/products/"):
            user = self.get_auth_user()
            if not user or user.get('role') != 'admin':
                return self.send_error_json("Forbidden: Admin access required", 403)
            try:
                prod_id = int(path.split('/')[-1])
                deleted = db.delete_product(prod_id)
                if not deleted:
                    return self.send_error_json("Product not found", 404)
                return self.send_json({"success": True, "message": "Product deleted successfully"})
            except Exception as e:
                return self.send_error_json(f"Delete failed: {str(e)}")
        else:
            self.send_error_json(f"Endpoint not found: DELETE {path}", 404)

    # --- Static File Server ---
    def serve_static_file(self, req_path):
        if req_path == "/" or req_path == "":
            req_path = "/index.html"
            
        clean_path = os.path.normpath(req_path.lstrip("/"))
        file_path = os.path.join(PUBLIC_DIR, clean_path)

        if not os.path.exists(file_path) or os.path.isdir(file_path):
            file_path = os.path.join(PUBLIC_DIR, "index.html")

        if os.path.exists(file_path) and os.path.isfile(file_path):
            content_type, _ = mimetypes.guess_type(file_path)
            if not content_type:
                content_type = "text/plain"
            if content_type.startswith("text/") or content_type == "application/javascript":
                content_type += "; charset=utf-8"

            try:
                with open(file_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(content)))
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_error_json(f"File read error: {str(e)}", 500)
        else:
            self.send_error_json("File not found", 404)

def run_server():
    db.init_db()
    try:
        import seed_data
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM products")
            if cursor.fetchone()['count'] == 0:
                print("Database is empty. Auto-seeding catalogue...")
                seed_data.seed_database(force_refresh=False)
    except Exception as e:
        print(f"Auto-seed check: {e}")
    with socketserver.TCPServer(("", PORT), StoreRequestHandler) as httpd:
        httpd.allow_reuse_address = True
        print(f"==================================================")
        print(f"  E-Commerce Store Server is running locally!     ")
        print(f"  URL: http://127.0.0.1:{PORT}                    ")
        print(f"==================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server gracefully...")

if __name__ == "__main__":
    run_server()
