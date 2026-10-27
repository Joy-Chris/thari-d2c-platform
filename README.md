# 🧵 Thari - Direct-to-Consumer (D2C) Handloom Marketplace

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-27%20Passing-brightgreen.svg)](tests/)

> **"Woven by Hand, Delivered from the Heart"**  
> A direct-to-consumer platform empowering traditional Indian handloom weavers by eliminating exploitative middlemen, authenticating Geographical Indication (GI) provenance, and ensuring **75% to 85% of retail price reaches the artisan directly**.

---

## 📖 Table of Contents
- [Mission & Heritage](#-mission--heritage)
- [Key Features](#-key-features)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Quickstart & Setup Steps](#-quickstart--setup-steps)
- [Environment Variables](#-environment-variables)
- [Running the Application](#-running-the-application)
- [Web Storefront & Pages](#-web-storefront--pages)
- [REST API Endpoints & cURL Examples](#-rest-api-endpoints--curl-examples)
- [Running the Test Suite](#-running-the-test-suite)
- [Submission Checklist Verification](#-submission-checklist-verification)
- [License](#-license)

---

## 🌾 Mission & Heritage

Traditional Indian handlooms represent centuries of cultural craftsmanship, mathematics, and sustainable slow fashion. However, in conventional retail:
- Intermediaries absorb up to **70% of the customer price**.
- Master weavers often earn less than daily agricultural wage rates.
- Powerloom fakes masquerade as genuine handloom without GI verification.

**Thari** re-engineers this supply chain:
1. **Direct Provenance:** Connects conscious patrons directly with certified artisan clusters (Chanderi, Kanchipuram, Pochampally Ikat, Jamdani Muslin, Sambalpuri Bandha, Maheshwari).
2. **Guaranteed Fair-Trade Share:** Enforces a minimum 75% (averaging 82%) direct payout per handwoven piece.
3. **Transparent Economic Breakdown:** Discloses artisan wages, yarn/zari raw material costs, artisanal packaging, and minimal platform escrow operations on every product card.
4. **Artisan Registration & Product Cataloging:** Allows weavers and cooperatives to register their looms, detail their lineage, and upload handwoven creations with technical metrics (loom days, yarn count, natural dyes).

---

## ✨ Key Features

- **FastAPI Modern Asynchronous Backend:** High-performance RESTful API with automated OpenAPI 3.0 / Swagger documentation.
- **Responsive Handloom-Themed UI/UX:** Warm earthy terracotta, raw silk, indigo, and gold zari color palette, crafted with typography inspired by Indian loom traditions.
- **Dynamic Storefront Catalog:** Real-time search and multi-facet filtering by craft tradition, Indian state/region, category, and price range.
- **Loom Story & Transparent Economics Modal:** Detailed view displaying the cultural story, loom days, yarn specifications, customer reviews, and a dynamic cost-breakdown bar chart.
- **Weaver Direct Messaging & Custom Queries:** Conscious patrons can message weavers directly to request custom dimensions or bespoke colorways.
- **Fair-Trade Escrow & Consignment Tracking:** Instant simulated checkout calculating direct artisan remittance and generating unique consignment tracking codes.
- **Artisan Onboarding Portal:** Simple, responsive interface for weavers and cooperatives to onboard and verify GI / Handloom Mark credentials.
- **Loom Creation Upload Portal:** Streamlined listing interface with live fair-wage preview calculation.

---

## 📂 Project Structure

```
THARI/
├── app/
│   ├── __init__.py               # Package initializer
│   ├── config.py                 # Pydantic Settings & environment variable configuration
│   ├── database.py             # In-memory thread-safe data access layer & seed loader
│   ├── schemas.py                # Pydantic v2 schemas for request & response validation
│   ├── main.py                   # FastAPI application initialization & route mounting
│   └── routers/
│       ├── __init__.py
│       ├── artisans.py           # Artisan registration, profile, and guild endpoints
│       ├── products.py           # Product upload, catalog filtering, details, reviews
│       ├── orders.py             # Customer checkout, order tracking, and escrow
│       ├── inquiries.py          # Direct consumer-to-weaver communication
│       └── storefront.py         # SSR HTML routes, healthcheck, and platform stats
├── static/
│   ├── css/
│   │   └── style.css             # Handloom-themed responsive stylesheet
│   └── js/
│       └── app.js                # Frontend client application (cart, modals, API calls)
├── templates/
│   ├── base.html                 # Base HTML layout, header, drawer, and modals
│   ├── index.html                # Main storefront catalog & live heritage impact stats
│   ├── artisans.html             # Master artisans directory & craft stories
│   ├── register_artisan.html     # Artisan registration portal
│   ├── upload_product.html       # Handloom creation upload portal
│   ├── orders.html               # Orders & direct weaver escrow tracker
│   └── transparent_pricing.html  # Fair-trade economic breakdown & comparison
├── data/
│   ├── artisans.json             # Sample master weavers & regional clusters
│   ├── products.json             # Sample authentic handloom creations
│   ├── categories.json           # Craft traditions, fibers, and product categories
│   └── orders.json               # Sample customer orders & consignment records
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Pytest fixtures and database test isolation
│   ├── test_artisans.py          # 9 test cases for artisan registration & profiles
│   ├── test_products.py          # 11 test cases for products, filtering, & reviews
│   └── test_orders.py            # 7 test cases for orders, inquiries, & stats
├── .env                          # Local environment variables
├── .env.example                  # Template of environment variables
├── requirements.txt              # Production and test dependencies
├── LICENSE                       # MIT License
├── TECHNICAL_DESIGN.md           # System architecture, Mermaid diagrams, & design
└── README.md                     # Project documentation (this file)
```

---

## 🛠 Prerequisites

- **Python:** 3.10 or higher (Python 3.11 recommended)
- **Pip:** 23.0+
- Modern Web Browser (Chrome, Firefox, Safari, Edge)

---

## 🚀 Quickstart & Setup Steps

### 1. Clone or Open the Workspace
```bash
cd c:\Users\LENOVO\Desktop\THARI
```

### 2. Create and Activate a Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

**On Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the template `.env.example` to `.env`:
```bash
cp .env.example .env
```
*(On Windows PowerShell, use `Copy-Item .env.example .env` if not already present)*

---

## ⚙️ Environment Variables

The application is configured using Pydantic Settings and supports variables defined in `.env` or system environment:

| Variable | Type | Default | Description |
| :--- | :---: | :---: | :--- |
| `APP_NAME` | `str` | `Thari` | Name of the application |
| `APP_TITLE` | `str` | `Thari - Handloom Weavers D2C Platform` | Title for FastAPI OpenAPI docs |
| `APP_DESCRIPTION` | `str` | *(Descriptive string)* | Summary of the platform |
| `APP_VERSION` | `str` | `1.0.0` | Semantic version |
| `DEBUG` | `bool` | `True` | Debug / hot reload flag |
| `HOST` | `str` | `0.0.0.0` | Bind host address |
| `PORT` | `int` | `8000` | Port for the HTTP server |
| `MIN_ARTISAN_SHARE_PERCENT` | `float` | `75.0` | Minimum guaranteed % paid to weavers |
| `DEFAULT_ARTISAN_SHARE_PERCENT` | `float` | `82.0` | Default fair-trade payout percentage |
| `PLATFORM_FEE_PERCENT` | `float` | `5.0` | Platform maintenance and escrow fee |
| `API_V1_PREFIX` | `str` | `/api/v1` | Routing prefix for REST API |
| `CORS_ORIGINS` | `list` | `["*"]` | Allowed CORS origins |
| `ENABLE_SIMULATED_ESCROW` | `bool` | `True` | Direct payment escrow simulation |
| `ENABLE_SAMPLE_DATA_SEEDING` | `bool` | `True` | Load sample data on startup |

---

## 🏃 Running the Application

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Alternatively, run directly with Python:
```bash
python -m app.main
```

Once started, access:
- **Responsive Storefront UI:** [http://localhost:8000](http://localhost:8000)
- **Interactive Swagger API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Alternative ReDoc Documentation:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **API Healthcheck:** [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

---

## 🖥 Web Storefront & Pages

| Route | View | Description |
| :--- | :--- | :--- |
| `/` | **Customer Storefront** | Curated catalog, search & multi-craft filters, live impact metrics, quick view modals, and cart drawer. |
| `/artisans-view` | **Master Weavers** | Directory of regional master weavers, guild affiliations, GI tags, and direct messaging. |
| `/register-artisan` | **Weaver Registration** | Form for artisans and cooperatives to register their looms and fair-trade parameters. |
| `/upload-product` | **List Handloom Creation** | Form for artisans to list products with yarn specs, loom days, and transparent pricing. |
| `/orders-view` | **Orders & Escrow** | Live registry of customer orders, tracking IDs, and direct weaver payouts. |
| `/transparency` | **Fair-Trade Economics** | Visual breakdown comparing conventional middleman retail vs. Thari's direct model. |

---

## 🔌 REST API Endpoints & cURL Examples

### 1. Register an Artisan
```bash
curl -X POST "http://localhost:8000/api/v1/artisans/register" \
     -H "Content-Type: application/json" \
     -d '{
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
     }'
```

### 2. Upload a Handloom Product
```bash
curl -X POST "http://localhost:8000/api/v1/products" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Sun-Bleached Kasavu Gold Zari Handloom Saree",
       "artisan_id": "art-001",
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
       "gi_tag_certified": true,
       "handloom_mark": true,
       "price_inr": 6500,
       "inventory_count": 4,
       "short_description": "Traditional Kerala handloom Kasavu saree crafted with delicate woven gold temple borders.",
       "detailed_story": "Woven with patience on a traditional pit loom, this Kasavu saree embodies timeless simplicity and cooling comfort for festivities."
     }'
```

### 3. Filter and Browse Catalog
```bash
# Filter by craft tradition
curl -X GET "http://localhost:8000/api/v1/products?craft=Ikat"

# Filter by price range and search term
curl -X GET "http://localhost:8000/api/v1/products?min_price=5000&max_price=15000&search=Chanderi"
```

### 4. Place a Customer Order (Direct Weaver Escrow)
```bash
curl -X POST "http://localhost:8000/api/v1/orders" \
     -H "Content-Type: application/json" \
     -d '{
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
     }'
```

### 5. Send Direct Inquiry to Weaver
```bash
curl -X POST "http://localhost:8000/api/v1/inquiries" \
     -H "Content-Type: application/json" \
     -d '{
       "artisan_id": "art-001",
       "product_id": "prod-001",
       "customer_name": "Shalini Gupta",
       "customer_email": "shalini.gupta@example.com",
       "customer_phone": "+91 98190 22334",
       "message": "Is it possible to weave this Chanderi saree in a custom deep emerald green colorway?",
       "custom_dimensions_requested": "Standard 6.4m"
     }'
```

---

## 🧪 Running the Test Suite

The test suite contains **27 comprehensive test cases** covering artisan workflows, product uploads, validation, storefront search/filters, customer reviews, order placement with stock deduction, and direct messaging.

Execute the tests with `pytest`:

```bash
pytest -v
```

Expected output:
```
tests/test_artisans.py::test_list_artisans PASSED                        [  3%]
tests/test_artisans.py::test_list_artisans_filter_by_state PASSED        [  7%]
tests/test_artisans.py::test_list_artisans_filter_by_craft PASSED        [ 11%]
tests/test_artisans.py::test_get_artisan_detail_success PASSED           [ 14%]
tests/test_artisans.py::test_get_artisan_detail_not_found PASSED         [ 18%]
tests/test_artisans.py::test_register_artisan_success PASSED             [ 22%]
tests/test_artisans.py::test_register_artisan_duplicate_email PASSED     [ 25%]
tests/test_artisans.py::test_update_artisan PASSED                       [ 29%]
tests/test_artisans.py::test_get_artisan_products PASSED                 [ 33%]
tests/test_orders.py::test_place_order_success PASSED                    [ 37%]
tests/test_orders.py::test_place_order_insufficient_stock PASSED         [ 40%]
tests/test_orders.py::test_list_orders PASSED                            [ 44%]
tests/test_orders.py::test_get_order_by_id PASSED                        [ 48%]
tests/test_orders.py::test_get_order_not_found PASSED                    [ 51%]
tests/test_orders.py::test_send_weaver_inquiry PASSED                    [ 55%]
tests/test_orders.py::test_platform_stats_and_health PASSED              [ 59%]
tests/test_products.py::test_list_products_default PASSED                [ 62%]
tests/test_products.py::test_filter_products_by_craft PASSED             [ 66%]
tests/test_products.py::test_filter_products_by_category PASSED          [ 70%]
tests/test_products.py::test_filter_products_by_price_range PASSED       [ 74%]
tests/test_products.py::test_search_products PASSED                      [ 77%]
tests/test_products.py::test_get_product_detail_success PASSED           [ 81%]
tests/test_products.py::test_get_product_detail_not_found PASSED         [ 85%]
tests/test_products.py::test_upload_product_success PASSED               [ 88%]
tests/test_products.py::test_upload_product_invalid_artisan PASSED       [ 92%]
tests/test_products.py::test_add_product_review PASSED                   [ 96%]
tests/test_products.py::test_delete_product PASSED                       [100%]

======================== 27 passed in 0.97s ========================
```

---

## ✅ Submission Checklist Verification

| Requirement | Artifact / Location | Status | Details |
| :--- | :--- | :---: | :--- |
| **1. ReadME Markdown** | `README.md` | ✅ **Complete** | Setup steps, prerequisites, environment variables, API examples, test instructions. |
| **2. Technical Design** | `TECHNICAL_DESIGN.md` | ✅ **Complete** | Full architecture, 4 detailed Mermaid diagrams (Architecture, ERD, Sequence, Data Flow). |
| **3. Sample Data Folder** | `data/` | ✅ **Complete** | `artisans.json`, `products.json`, `categories.json`, `orders.json` with rich handloom data. |
| **4. Tests Folder** | `tests/` | ✅ **Complete** | 27 pytest test cases covering all CRUD, validation, and escrow logic (`conftest.py`, `test_artisans.py`, `test_products.py`, `test_orders.py`). |
| **5. License File** | `LICENSE` | ✅ **Complete** | Standard MIT License. |

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
