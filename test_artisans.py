import pytest

def test_list_artisans(client):
    response = client.get("/api/v1/artisans")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 5
    # Verify fields in artisan response
    first = data[0]
    assert "id" in first
    assert "full_name" in first
    assert "cluster_name" in first
    assert "craft_tradition" in first
    assert "fair_trade_share_percent" in first

def test_list_artisans_filter_by_state(client):
    response = client.get("/api/v1/artisans?state=Madhya Pradesh")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    for artisan in data:
        assert artisan["state"] == "Madhya Pradesh"

def test_list_artisans_filter_by_craft(client):
    response = client.get("/api/v1/artisans?craft=Ikat")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any("Ikat" in a["craft_tradition"] for a in data)

def test_get_artisan_detail_success(client):
    response = client.get("/api/v1/artisans/art-001")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "art-001"
    assert "Devendra" in data["full_name"]
    assert data["cluster_name"] == "Chanderi Weavers Collective"
    assert data["fair_trade_share_percent"] == 82.0

def test_get_artisan_detail_not_found(client):
    response = client.get("/api/v1/artisans/art-unknown-999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_register_artisan_success(client):
    new_artisan = {
        "full_name": "Gopalakrishnan Chettiar",
        "cluster_name": "Chettinad Cotton Weavers Sangam",
        "craft_tradition": "Chettinad Cotton Kandangi",
        "loom_type": "Raised Pit Loom",
        "village": "Kanadukathan",
        "district": "Sivaganga",
        "state": "Tamil Nadu",
        "experience_years": 32,
        "bio": "Specialist in traditional thick earthy mustard and maroon Kandangi checks, preserving heirloom Tamil weaving for four decades.",
        "phone": "+91 94431 00223",
        "email": "gopal.chettinad@thari.org",
        "certifications": ["GI Tag TN-011", "Handloom Mark"],
        "fair_trade_share_percent": 84.0,
        "active_looms": 4
    }
    response = client.post("/api/v1/artisans/register", json=new_artisan)
    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == "Gopalakrishnan Chettiar"
    assert data["id"].startswith("art-")
    assert data["fair_trade_share_percent"] == 84.0

    # Verify artisan is now retrievable
    art_id = data["id"]
    get_resp = client.get(f"/api/v1/artisans/{art_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["email"] == "gopal.chettinad@thari.org"

def test_register_artisan_duplicate_email(client):
    duplicate = {
        "full_name": "Devendra Twin",
        "cluster_name": "Chanderi Cluster",
        "craft_tradition": "Chanderi",
        "loom_type": "Pit Loom",
        "village": "Pranpur",
        "district": "Ashoknagar",
        "state": "Madhya Pradesh",
        "experience_years": 15,
        "bio": "Another weaver working in the Chanderi craft tradition.",
        "phone": "+91 99999 11111",
        "email": "devendra.chanderi@thari.org", # already in seed data
        "certifications": ["Handloom Mark"],
        "fair_trade_share_percent": 80.0
    }
    response = client.post("/api/v1/artisans/register", json=duplicate)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()

def test_update_artisan(client):
    update_payload = {
        "bio": "Updated biography highlighting 29 years of heritage mastery.",
        "active_looms": 5
    }
    response = client.put("/api/v1/artisans/art-001", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["bio"] == "Updated biography highlighting 29 years of heritage mastery."
    assert data["active_looms"] == 5

def test_get_artisan_products(client):
    response = client.get("/api/v1/artisans/art-001/products")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    for p in data:
        assert p["artisan_id"] == "art-001"
