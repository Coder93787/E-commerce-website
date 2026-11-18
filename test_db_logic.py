"""
Direct Unit & Integration Tests for E-Commerce Store Logic.
Tests database, auth, catalogue, cart deduction, order placement, and payments.
Runs completely offline without loopback sockets.
"""
import database as db
import secrets
import time

def run():
    print(">>> Initializing and Seeding Database...")
    db.init_db()

    # 1. Product queries
    products = db.get_products()
    assert len(products) >= 12, f"Expected at least 12 products, got {len(products)}"
    print(f"✓ Products count: {len(products)}")

    # 2. Categories
    cats = db.get_categories()
    assert len(cats) >= 3, f"Expected categories, got {cats}"
    print(f"✓ Categories: {cats}")

    # 3. Category Filter
    fashion = db.get_products(category="Fashion")
    assert len(fashion) >= 2
    for p in fashion:
        assert p['category'].lower() == 'fashion'
    print(f"✓ Category filter verified ({len(fashion)} items)")

    # 4. Search Filter
    jeans = db.get_products(search="Jeans")
    assert len(jeans) >= 1
    assert "jeans" in jeans[0]['title'].lower()
    print("✓ Search query verified")

    # 5. User Registration & Auth
    test_email = f"test_{int(time.time())}@example.com"
    user_id = db.create_user("Test Buyer", test_email, "TestPass123!", role="customer")
    assert user_id > 0
    print(f"✓ Created test buyer with ID: {user_id}")

    # Authenticate
    auth_data = db.authenticate_user(test_email, "TestPass123!")
    assert auth_data is not None
    token = auth_data["token"]
    user_info = db.get_user_by_token(token)
    assert user_info["email"] == test_email
    print("✓ Auth token validated successfully")

    # 6. Admin Authentication
    admin_auth = db.authenticate_user("admin@store.com", "Admin@123")
    assert admin_auth is not None
    assert admin_auth["user"]["role"] == "admin"
    print("✓ Admin authentication verified")

    # 7. Heavy Feature: Payment & Order Execution Logic
    # Test Failed Payment:
    tx_fail = f"ch_test_fail_{secrets.token_hex(4)}"
    db.record_payment_log(
        tx_ref=tx_fail,
        user_id=user_id,
        gateway="stripe",
        amount=149.99,
        status="failed",
        card_last4="0002",
        error_message="Card declined: Insufficient funds (Simulated)"
    )
    # Check that NO order exists for user_id
    user_orders = db.get_user_orders(user_id)
    assert len(user_orders) == 0, "No orders should exist after failed payment!"
    print("✓ Failed payment logged, order correctly omitted.")

    # Test Successful Payment:
    initial_stock = products[0]['stock']
    p_id = products[0]['id']
    tx_success = f"ch_test_success_{secrets.token_hex(4)}"
    
    order = db.create_order_after_payment(
        user_id=user_id,
        customer_name="Test Buyer",
        customer_email=test_email,
        shipping_address="742 Evergreen Terrace, Springfield",
        cart_items=[{"product_id": p_id, "quantity": 2}],
        gateway="stripe",
        payment_id=tx_success
    )
    db.record_payment_log(
        tx_ref=tx_success,
        user_id=user_id,
        gateway="stripe",
        amount=order['total_amount'],
        status="succeeded",
        card_last4="4242"
    )

    # Check order was created
    assert order["status"] == "paid"
    assert "ORD-" in order["order_number"]
    assert len(order["items"]) == 1
    assert order["items"][0]["quantity"] == 2
    
    # Check stock was decremented by 2
    updated_p = db.get_product(p_id)
    assert updated_p['stock'] == initial_stock - 2, f"Stock should be {initial_stock - 2}, got {updated_p['stock']}"
    print(f"✓ Stock decremented from {initial_stock} to {updated_p['stock']}.")

    # Check user order history
    my_orders = db.get_user_orders(user_id)
    assert len(my_orders) == 1
    assert my_orders[0]['order_number'] == order['order_number']
    print(f"✓ Order history retrieved with order number: {order['order_number']}")

    # 8. Admin Operations
    # Add product
    new_pid = db.add_product({
        "title": "Minimalist Emerald Desk Mat",
        "description": "Premium vegan leather desk mat in deep forest green",
        "price": 38.0,
        "category": "Accessories",
        "image_url": "https://example.com/mat.jpg",
        "stock": 10,
        "rating": 4.9,
        "is_featured": 1
    })
    assert new_pid > 0
    print(f"✓ Admin added new product ID: {new_pid}")

    # Edit product
    db.update_product(new_pid, {
        "title": "Minimalist Emerald Desk Mat (Large)",
        "description": "Premium vegan leather desk mat in deep forest green",
        "price": 42.0,
        "category": "Accessories",
        "image_url": "https://example.com/mat.jpg",
        "stock": 20,
        "is_featured": 1
    })
    edited_p = db.get_product(new_pid)
    assert edited_p['price'] == 42.0
    assert edited_p['stock'] == 20
    print("✓ Admin updated product verified")

    # Update order status
    db.update_order_status(order['order_id'], "shipped")
    updated_order = [o for o in db.get_all_orders() if o['id'] == order['order_id']][0]
    assert updated_order['status'] == "shipped"
    print("✓ Admin updated order status to 'shipped'")

    # Delete product
    db.delete_product(new_pid)
    assert db.get_product(new_pid) is None
    print("✓ Admin deleted product verified")

    # Metrics
    metrics = db.get_admin_metrics()
    assert metrics['total_orders'] >= 1
    assert metrics['total_revenue'] > 0
    print(f"✓ Admin metrics verified: {metrics}")

    print("\n=============================================")
    print("  ALL BACKEND LOGIC & INTEGRATION TESTS PASS! ")
    print("=============================================")

if __name__ == "__main__":
    run()
