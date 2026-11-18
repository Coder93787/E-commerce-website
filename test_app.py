"""
Automated Integration Tests for E-Commerce Store
Runs the server in a background thread and tests all REST endpoints.
"""
import threading
import time
import urllib.request
import urllib.error
import json
import socketserver
import os
import sys

from server import StoreRequestHandler, PORT
import database as db

BASE_URL = f"http://127.0.0.1:{PORT}"

def run_test_server():
    httpd = socketserver.TCPServer(("", PORT), StoreRequestHandler)
    httpd.allow_reuse_address = True
    httpd.serve_forever()

def request(method, path, data=None, token=None):
    url = f"{BASE_URL}{path}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    body = json.dumps(data).encode('utf-8') if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode('utf-8')
            return resp.status, json.loads(content) if content else {}
    except urllib.error.HTTPError as e:
        content = e.read().decode('utf-8')
        try:
            return e.code, json.loads(content)
        except:
            return e.code, {"raw": content}

def run_tests():
    print(">>> Starting test server thread...")
    t = threading.Thread(target=run_test_server, daemon=True)
    t.start()
    time.sleep(1) # wait for server to bind

    # Ensure database is seeded
    import seed_data
    seed_data.seed_database()

    print("\n--- TEST 1: Fetch Products ---")
    status, res = request("GET", "/api/products")
    assert status == 200, f"Expected 200, got {status}"
    assert res["success"] is True
    assert len(res["products"]) >= 12
    print(f"✓ Successfully fetched {len(res['products'])} products.")

    print("\n--- TEST 2: Filter by Category ---")
    status, res = request("GET", "/api/products?category=Footwear")
    assert status == 200
    for p in res["products"]:
        assert p["category"] == "Footwear"
    print(f"✓ Category filter works: {len(res['products'])} Footwear items returned.")

    print("\n--- TEST 3: Live Search Query ---")
    status, res = request("GET", "/api/products?search=runner")
    assert status == 200
    assert len(res["products"]) >= 1
    assert "Runner" in res["products"][0]["title"]
    print("✓ Product search works.")

    print("\n--- TEST 4: User Registration & Authentication ---")
    test_email = f"tester_{int(time.time())}@example.com"
    status, res = request("POST", "/api/auth/register", {
        "name": "Jane Tester",
        "email": test_email,
        "password": "Password123!"
    })
    assert status == 201, f"Register failed: {res}"
    user_token = res["token"]
    assert user_token is not None
    print("✓ Customer registered successfully.")

    print("\n--- TEST 5: Validate Auth Token (/api/auth/me) ---")
    status, res = request("GET", "/api/auth/me", token=user_token)
    assert status == 200
    assert res["user"]["email"] == test_email
    print("✓ Auth token validated.")

    print("\n--- TEST 6: Heavy Feature - FAILED Payment Gateway Flow ---")
    # Simulate payment failure: Order must NOT be created!
    fail_payload = {
        "gateway": "stripe",
        "test_action": "fail",
        "customer_name": "Jane Tester",
        "customer_email": test_email,
        "shipping_address": "456 Test Ave, City, Country",
        "cart_items": [{"product_id": 1, "price": 149.99, "quantity": 1}],
        "payment_info": {"card_number": "4000 0000 0000 0002", "expiry": "12/28", "cvv": "123"}
    }
    status, res = request("POST", "/api/payments/process", fail_payload, token=user_token)
    assert status == 402, f"Expected 402 Payment Required, got {status} - {res}"
    assert res["success"] is False
    assert "declined" in res["error"].lower()
    
    # Confirm NO order was created for this user
    status, res = request("GET", "/api/orders/my-orders", token=user_token)
    assert status == 200
    assert len(res["orders"]) == 0, "No orders should exist after failed payment!"
    print("✓ Failed payment handled correctly: 402 returned and NO order was generated.")

    print("\n--- TEST 7: Heavy Feature - SUCCESSFUL Payment Gateway Flow ---")
    success_payload = {
        "gateway": "stripe",
        "test_action": "success",
        "customer_name": "Jane Tester",
        "customer_email": test_email,
        "shipping_address": "456 Test Ave, City, Country",
        "cart_items": [{"product_id": 1, "price": 149.99, "quantity": 1}],
        "payment_info": {"card_number": "4242 4242 4242 4242", "expiry": "12/28", "cvv": "123"}
    }
    status, res = request("POST", "/api/payments/process", success_payload, token=user_token)
    assert status == 200, f"Payment process failed: {res}"
    assert res["success"] is True
    assert "ORD-" in res["order"]["order_number"]
    assert res["order"]["status"] == "paid"
    print(f"✓ Successful payment processed: Order {res['order']['order_number']} created.")

    print("\n--- TEST 8: Customer Order History ---")
    status, res = request("GET", "/api/orders/my-orders", token=user_token)
    assert status == 200
    assert len(res["orders"]) == 1
    assert len(res["orders"][0]["items"]) == 1
    print("✓ Order history retrieves order with items.")

    print("\n--- TEST 9: Admin Authorization & Controls ---")
    # Log in as admin
    status, res = request("POST", "/api/auth/login", {
        "email": "admin@store.com",
        "password": "Admin@123"
    })
    assert status == 200
    admin_token = res["token"]
    assert res["user"]["role"] == "admin"

    # Admin Metrics
    status, res = request("GET", "/api/admin/metrics", token=admin_token)
    assert status == 200
    assert res["metrics"]["total_products"] >= 12
    print(f"✓ Admin metrics: {res['metrics']}")

    # Admin Create Product
    new_prod_data = {
        "title": "Test Emerald Cap",
        "description": "Premium 6-panel cap with emerald brim",
        "price": 28.00,
        "category": "Accessories",
        "image_url": "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?auto=format&fit=crop&w=800&q=80",
        "stock": 15,
        "is_featured": 0
    }
    status, res = request("POST", "/api/admin/products", new_prod_data, token=admin_token)
    assert status == 201
    created_id = res["product_id"]
    print(f"✓ Admin created new product ID: {created_id}")

    # Admin Edit Product
    new_prod_data["price"] = 24.50
    status, res = request("PUT", f"/api/admin/products/{created_id}", new_prod_data, token=admin_token)
    assert status == 200
    print("✓ Admin updated product price.")

    # Admin Delete Product
    status, res = request("DELETE", f"/api/admin/products/{created_id}", token=admin_token)
    assert status == 200
    print("✓ Admin deleted product.")

    print("\n==========================================")
    print("  ALL 9 INTEGRATION TESTS PASSED 100%!   ")
    print("==========================================")

if __name__ == "__main__":
    run_tests()
