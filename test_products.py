import pytest

def test_list_products_default(client):
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 6
    first = data[0]
    assert "id" in first
    assert "title" in first
    assert "price_inr" in first
    assert "loom_days" in first
    assert "transparent_pricing" in first
    assert "artisan" in first

def test_filter_products_by_craft(client):
    response = client.get("/api/v1/products?craft=Ikat")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    for p in data:
        assert "ikat" in p["craft_tradition"].lower()

def test_filter_products_by_category(client):
    response = client.get("/api/v1/products?category=Dupattas%20%26%20Stoles")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    for p in data:
        assert p["category"] == "Dupattas & Stoles"

def test_filter_products_by_price_range(client):
    response = client.get("/api/v1/products?min_price=10000&max_price=20000")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    for p in data:
        assert 10000 <= p["price_inr"] <= 20000

def test_search_products(client):
    response = client.get("/api/v1/products?search=Ashrafi")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert "Ashrafi" in data[0]["title"]

def test_get_product_detail_success(client):
    response = client.get("/api/v1/products/prod-001")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "prod-001"
    assert data["artisan_id"] == "art-001"
    assert data["artisan"]["full_name"] == "Devendra Kumar Ansari"
    assert data["transparent_pricing"]["artisan_wages"] > 0
    assert len(data["reviews"]) >= 1

def test_get_product_detail_not_found(client):
    response = client.get("/api/v1/products/prod-non-existent")
    assert response.status_code == 404

def test_upload_product_success(client):
    new_product = {
        "title": "Sun-Bleached Kasavu Gold Zari Handloom Saree",
        "artisan_id": "art-002",
        "craft_tradition": "Balaramapuram Kasavu",
        "category": "Sarees",
        "material": "100% Unbleached Fine Cotton & Pure Zari",
        "warp_yarn": "100s Combed Cotton",
        "weft_yarn": "100s Combed Cotton with Half-Fine Zari",
        "loom_type": "Traditional Pit Loom",
        "loom_days": 10,
        "dimensions": "6.25 meters",
        "color": "Off-White & Muted Gold",
        "dye_type": "Unbleached Natural Cotton",
        "gi_tag_certified": True,
        "handloom_mark": True,
        "price_inr": 6500,
        "inventory_count": 4,
        "short_description": "Traditional Kerala handloom Kasavu saree crafted with delicate woven gold temple borders.",
        "detailed_story": "Woven with patience on a traditional pit loom, this Kasavu saree embodies timeless simplicity and cooling comfort for festivities.",
        "images": [
            "https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=1000&q=80"
        ],
        "is_featured": True,
        "care_instructions": "Hand wash gently in cold water.",
        "origin_cluster": "Balaramapuram, Kerala"
    }
    response = client.post("/api/v1/products", json=new_product)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Sun-Bleached Kasavu Gold Zari Handloom Saree"
    assert data["id"].startswith("prod-")
    assert "transparent_pricing" in data
    # Verify calculated fair wages is at least 75%
    wages = data["transparent_pricing"]["artisan_wages"]
    assert wages >= 6500 * 0.75

def test_upload_product_invalid_artisan(client):
    bad_product = {
        "title": "Invalid Artisan Product Test",
        "artisan_id": "art-ghost-000",
        "craft_tradition": "Unknown",
        "category": "Sarees",
        "material": "Silk",
        "loom_days": 5,
        "dimensions": "6m",
        "color": "Red",
        "price_inr": 5000,
        "inventory_count": 1,
        "short_description": "Short description for validation test here.",
        "detailed_story": "Detailed story that meets the minimum length requirement for testing purposes."
    }
    response = client.post("/api/v1/products", json=bad_product)
    assert response.status_code == 404
    assert "does not exist" in response.json()["detail"].lower()

def test_add_product_review(client):
    review_data = {
        "customer_name": "Meera Krishnan",
        "rating": 5,
        "comment": "Sublime drape and authentic handloom texture. Truly empowers our master weavers!"
    }
    response = client.post("/api/v1/products/prod-002/reviews", json=review_data)
    assert response.status_code == 201
    data = response.json()
    assert data["customer_name"] == "Meera Krishnan"
    assert data["rating"] == 5
    assert data["product_id"] == "prod-002"

    # Confirm it appears in product details
    prod_resp = client.get("/api/v1/products/prod-002")
    reviews = prod_resp.json()["reviews"]
    assert any(r["customer_name"] == "Meera Krishnan" for r in reviews)

def test_delete_product(client):
    # Upload temporary product then delete it
    temp_prod = {
        "title": "Temporary Product to Delete",
        "artisan_id": "art-001",
        "craft_tradition": "Chanderi",
        "category": "Dupattas & Stoles",
        "material": "Cotton",
        "loom_days": 3,
        "dimensions": "2m",
        "color": "Blue",
        "price_inr": 2000,
        "inventory_count": 1,
        "short_description": "Short description for temporary item.",
        "detailed_story": "Detailed story for temporary item that will be deleted right after creation."
    }
    create_resp = client.post("/api/v1/products", json=temp_prod)
    assert create_resp.status_code == 201
    prod_id = create_resp.json()["id"]

    # Delete
    del_resp = client.delete(f"/api/v1/products/{prod_id}")
    assert del_resp.status_code == 204

    # Verify not found
    get_resp = client.get(f"/api/v1/products/{prod_id}")
    assert get_resp.status_code == 404
