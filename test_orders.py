import pytest

def test_place_order_success(client):
    order_payload = {
        "customer_name": "Siddharth Nambiar",
        "customer_email": "siddharth@example.com",
        "customer_phone": "+91 98200 45678",
        "shipping_address": {
            "street": "44 Palm Grove Road",
            "city": "Mumbai",
            "state": "Maharashtra",
            "pincode": "400050",
            "country": "India"
        },
        "items": [
            {
                "product_id": "prod-001",
                "quantity": 1
            }
        ],
        "payment_method": "UPI / Direct Weaver Escrow"
    }

    # Check inventory before order
    prod_before = client.get("/api/v1/products/prod-001").json()
    stock_before = prod_before["inventory_count"]

    response = client.post("/api/v1/orders", json=order_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["order_id"].startswith("ORD-")
    assert data["payment_status"] == "PAID"
    assert data["total_inr"] == 12800.0
    assert data["total_artisan_direct_payout_inr"] > 10000.0
    assert "tracking_number" in data

    # Verify inventory was decremented
    prod_after = client.get("/api/v1/products/prod-001").json()
    assert prod_after["inventory_count"] == stock_before - 1

def test_place_order_insufficient_stock(client):
    order_payload = {
        "customer_name": "Bulk Buyer",
        "customer_email": "bulk@example.com",
        "customer_phone": "+91 99999 88888",
        "shipping_address": {
            "street": "10 Commercial Street",
            "city": "Bengaluru",
            "state": "Karnataka",
            "pincode": "560001",
            "country": "India"
        },
        "items": [
            {
                "product_id": "prod-002",
                "quantity": 5 # Available stock is only 2
            }
        ]
    }
    response = client.post("/api/v1/orders", json=order_payload)
    assert response.status_code == 400
    assert "insufficient stock" in response.json()["detail"].lower()

def test_list_orders(client):
    response = client.get("/api/v1/orders")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2 # Seed orders exist

def test_get_order_by_id(client):
    response = client.get("/api/v1/orders/ORD-2026-8801")
    assert response.status_code == 200
    data = response.json()
    assert data["order_id"] == "ORD-2026-8801"
    assert data["customer_name"] == "Aarav Sharma"
    assert data["payment_status"] == "PAID"

def test_get_order_not_found(client):
    response = client.get("/api/v1/orders/ORD-FAKE-999")
    assert response.status_code == 404

def test_send_weaver_inquiry(client):
    inquiry_payload = {
        "artisan_id": "art-001",
        "product_id": "prod-001",
        "customer_name": "Shalini Gupta",
        "customer_email": "shalini.gupta@example.com",
        "customer_phone": "+91 98190 22334",
        "message": "Hello Devendraji, is it possible to weave this Chanderi saree in a custom deep emerald green colorway?",
        "custom_dimensions_requested": "Standard 6.4m"
    }
    response = client.post("/api/v1/inquiries", json=inquiry_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"].startswith("inq-")
    assert data["artisan_id"] == "art-001"
    assert data["status"] == "PENDING_ARTISAN_RESPONSE"

    # Verify listing inquiries for this artisan
    list_resp = client.get("/api/v1/inquiries/artisan/art-001")
    assert list_resp.status_code == 200
    assert any(i["customer_name"] == "Shalini Gupta" for i in list_resp.json())

def test_platform_stats_and_health(client):
    health_resp = client.get("/api/v1/health")
    assert health_resp.status_code == 200
    assert health_resp.json()["status"] == "healthy"

    stats_resp = client.get("/api/v1/stats")
    assert stats_resp.status_code == 200
    stats = stats_resp.json()
    assert stats["total_artisans"] >= 5
    assert stats["total_products"] >= 6
    assert stats["average_fair_share_percent"] >= 75.0
