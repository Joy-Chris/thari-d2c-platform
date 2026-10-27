# 📐 Thari - Technical Design Document

**Project:** Thari Handloom D2C Platform  
**Architecture Version:** 1.0.0  
**Status:** Approved & Implemented  
**Date:** October 2026  

---

## 1. Executive Summary & Design Philosophy

**Thari** is an ethical, Direct-to-Consumer (D2C) marketplace platform engineered to bridge Indian traditional handloom weavers directly with conscious consumers. The platform solves the chronic exploitation of weavers in conventional retail supply chains—where intermediaries pocket up to 70% of retail margins—by guaranteeing that **75% to 85% of retail price is remitted directly into the artisan's hands**.

### Core Architectural Principles:
1. **Radical Transparency:** Every product record contains structured mathematical cost breakdowns (artisan labor wages, raw materials, finishing, and escrow ops).
2. **Provenance-First Data Model:** Products are intrinsically tied to certified artisans, geographic coordinates/clusters, loom mechanisms, and Geographical Indication (GI) tag verifications.
3. **High Performance & Asynchronous Operations:** Built atop FastAPI and Python 3.11 for non-blocking I/O, strict Pydantic validation, and low latency.
4. **Zero-Dependency Native Frontend:** Responsive, accessible handloom-themed UI rendered via Jinja2 SSR and vanilla ES6 client logic without complex Node/bundler overhead.

---

## 2. High-Level System Architecture

The following diagram illustrates the multi-tier system topology of Thari:

```mermaid
flowchart TD
    subgraph Client_Tier ["Client & Interaction Tier"]
        C1["Conscious Consumer (Mobile / Web Browser)"]
        C2["Master Weaver / Cooperative Manager"]
        C3["API Consumers / Automated Clients"]
    end

    subgraph Gateway_Tier ["FastAPI Gateway & Presentation Layer"]
        GW["FastAPI Core Engine (ASGI / Uvicorn)"]
        CORS["CORS & Request Middleware"]
        STATIC["Static Asset Handler (/static/css, /static/js)"]
        SSR["Jinja2 SSR Template Engine (Storefront Views)"]
    end

    subgraph Service_Tier ["Application & Domain Services"]
        ART_SVC["Artisan Registry Service"]
        PROD_SVC["Handloom Catalog & Provenance Service"]
        ORD_SVC["Order Placement & Fair Escrow Service"]
        INQ_SVC["Direct Weaver Messaging Service"]
        STAT_SVC["Platform Impact & Analytics Service"]
    end

    subgraph Schema_Tier ["Validation & Policy Engine"]
        PY_SCHEMAS["Pydantic v2 Models & Validators"]
        FAIR_POLICY["Fair-Trade Payout Rule (Min 75% Weaver Share)"]
        GI_VERIFY["GI Tag & Handloom Mark Accreditation Guard"]
    end

    subgraph Persistence_Tier ["Data & Storage Layer"]
        MEM_DB["Thari Thread-Safe In-Memory Store"]
        JSON_SEEDS["Seed Repositories (/data/*.json)"]
        DB_ARTISANS["data/artisans.json"]
        DB_PRODUCTS["data/products.json"]
        DB_ORDERS["data/orders.json"]
        DB_CATEGORIES["data/categories.json"]
    end

    C1 -->|Browse Catalog & Order| GW
    C2 -->|Register & Upload Weaves| GW
    C3 -->|REST API Invocations| GW

    GW --> CORS
    CORS --> SSR
    CORS --> STATIC
    CORS --> PY_SCHEMAS

    PY_SCHEMAS --> FAIR_POLICY
    PY_SCHEMAS --> GI_VERIFY

    PY_SCHEMAS --> ART_SVC
    PY_SCHEMAS --> PROD_SVC
    PY_SCHEMAS --> ORD_SVC
    PY_SCHEMAS --> INQ_SVC
    PY_SCHEMAS --> STAT_SVC

    ART_SVC --> MEM_DB
    PROD_SVC --> MEM_DB
    ORD_SVC --> MEM_DB
    INQ_SVC --> MEM_DB
    STAT_SVC --> MEM_DB

    MEM_DB -.->|Initial Bootstrap| JSON_SEEDS
    JSON_SEEDS --> DB_ARTISANS
    JSON_SEEDS --> DB_PRODUCTS
    JSON_SEEDS --> DB_ORDERS
    JSON_SEEDS --> DB_CATEGORIES
```

---

## 3. Entity-Relationship Model (Data Architecture)

The data model connects artisans with their handloom creations, customer reviews, direct inquiries, and customer orders with itemized fair-trade shares:

```mermaid
erDiagram
    ARTISAN ||--o{ PRODUCT : "crafts and lists"
    ARTISAN ||--o{ INQUIRY : "receives direct messages"
    PRODUCT ||--o{ REVIEW : "receives patron reviews"
    PRODUCT ||--o{ ORDER_ITEM : "is purchased in"
    ORDER ||--|{ ORDER_ITEM : "contains"
    PRODUCT ||--|| TRANSPARENT_PRICING : "defines cost breakdown"

    ARTISAN {
        string id PK
        string full_name
        string cluster_name
        string craft_tradition
        string loom_type
        string village
        string district
        string state
        int experience_years
        string bio
        string phone
        string email
        string_array certifications
        float fair_trade_share_percent
        int active_looms
        float rating
        int review_count
        datetime created_at
    }

    PRODUCT {
        string id PK
        string artisan_id FK
        string title
        string craft_tradition
        string category
        string material
        string warp_yarn
        string weft_yarn
        string loom_type
        int loom_days
        string dimensions
        string color
        string dye_type
        boolean gi_tag_certified
        boolean handloom_mark
        float price_inr
        int inventory_count
        string short_description
        string detailed_story
        string_array images
        boolean is_featured
        string care_instructions
        string origin_cluster
        datetime created_at
    }

    TRANSPARENT_PRICING {
        float artisan_wages
        float raw_material_silk_zari
        float finishing_packaging
        float platform_fair_trade_ops
    }

    ORDER {
        string order_id PK
        string customer_name
        string customer_email
        string customer_phone
        json shipping_address
        float subtotal_inr
        float shipping_fee_inr
        float total_inr
        float total_artisan_direct_payout_inr
        string payment_status
        string payment_method
        string order_status
        string tracking_number
        datetime created_at
        string weavers_note
    }

    ORDER_ITEM {
        string product_id FK
        string title
        int quantity
        float unit_price_inr
        string artisan_id FK
        float artisan_share_inr
    }

    INQUIRY {
        string id PK
        string artisan_id FK
        string product_id FK
        string customer_name
        string customer_email
        string customer_phone
        string message
        string custom_dimensions_requested
        string status
        datetime created_at
    }

    REVIEW {
        string id PK
        string product_id FK
        string customer_name
        int rating
        string comment
        boolean verified_purchase
        datetime created_at
    }
```

---

## 4. Sequence Diagrams

### 4.1. Customer Storefront Order Placement & Fair Escrow Settlement

```mermaid
sequenceDiagram
    autonumber
    actor Customer as Conscious Patron
    participant UI as Thari Storefront UI
    participant OrderAPI as /api/v1/orders
    participant DB as Thari Database Store
    participant Escrow as Weaver Escrow Ledger

    Customer->>UI: Select Handloom & Click "Place Order"
    UI->>OrderAPI: POST /api/v1/orders (Customer & Items Payload)
    
    activate OrderAPI
    OrderAPI->>DB: Check Product Existence & Inventory Availability
    
    alt Stock Insufficient
        DB-->>OrderAPI: Inventory < Requested Quantity
        OrderAPI-->>UI: 400 Bad Request ("Insufficient stock for creation")
        UI-->>Customer: Display Out of Stock notification
    else Stock Available
        OrderAPI->>DB: Atomically decrement product inventory
        OrderAPI->>DB: Lookup Weaver fair_trade_share_percent (e.g. 82%)
        OrderAPI->>OrderAPI: Calculate Line Artisan Payout = Price * (Share / 100)
        OrderAPI->>Escrow: Credit Escrow Account for Weaver
        OrderAPI->>DB: Commit Order Record with Tracking ID
        DB-->>OrderAPI: Order Confirmation Record
        OrderAPI-->>UI: 201 Created (OrderResponse + Tracking ID)
        deactivate OrderAPI
        UI-->>Customer: Render Order Confirmation Modal with Consignment Code
    end
```

### 4.2. Artisan Onboarding & Handloom Product Upload Workflow

```mermaid
sequenceDiagram
    autonumber
    actor Weaver as Master Weaver / Cooperative
    participant Portal as Weaver Portal UI
    participant ArtisanAPI as /api/v1/artisans/register
    participant ProductAPI as /api/v1/products
    participant DB as Thari Database Store

    Weaver->>Portal: Submit Artisan Profile (Cluster, Loom Type, GI Tag, Share %)
    Portal->>ArtisanAPI: POST /api/v1/artisans/register
    activate ArtisanAPI
    ArtisanAPI->>DB: Check for duplicate email
    ArtisanAPI->>DB: Store Artisan Record
    DB-->>ArtisanAPI: Artisan Created (art-XXXX)
    ArtisanAPI-->>Portal: 201 Created
    deactivate ArtisanAPI

    Weaver->>Portal: Upload Handloom Creation (Yarns, Loom Days, Story, Price)
    Portal->>ProductAPI: POST /api/v1/products
    activate ProductAPI
    ProductAPI->>DB: Verify Artisan ID Exists
    ProductAPI->>ProductAPI: Compute Transparent Pricing breakdown (82% labor)
    ProductAPI->>DB: Persist Product & Link to Artisan
    DB-->>ProductAPI: Product Created (prod-XXXX)
    ProductAPI-->>Portal: 201 Created
    deactivate ProductAPI
    Portal-->>Weaver: Success! Piece published immediately to consumer storefront
```

---

## 5. Data Flow Diagram (DFD - Level 1)

```mermaid
flowchart LR
    P[Patron / Buyer]
    W[Weaver / Cooperative]

    subgraph THARI_PLATFORM ["Thari Platform Core Engine"]
        F1["1.0 Artisan Onboarding"]
        F2["2.0 Catalog & Search Engine"]
        F3["3.0 Fair Escrow Order Processing"]
        F4["4.0 Direct Weaver Messaging"]
        F5["5.0 Impact Analytics"]
    end

    subgraph DATA_STORES ["Data Stores"]
        D1[("Artisans Store")]
        D2[("Products Store")]
        D3[("Orders Store")]
        D4[("Inquiries Store")]
    end

    W -->|Registration Details| F1
    F1 -->|Save Profile| D1

    W -->|Loom Specs & Pricing| F2
    D1 -.->|Verify Lineage| F2
    F2 -->|Save Creation| D2

    P -->|Search & Filter Query| F2
    D2 -->|Return Curated Weaves| F2
    F2 -->|Catalog View| P

    P -->|Cart Checkout| F3
    D2 -->|Validate Stock| F3
    F3 -->|Deduct Stock| D2
    D1 -->|Read Fair Share %| F3
    F3 -->|Record Order & Payout| D3
    F3 -->|Consignment Tracking| P

    P -->|Custom Query / Message| F4
    F4 -->|Record Inquiry| D4
    D4 -->|Alert Artisan| W

    D1 & D2 & D3 -->|Aggregate Metrics| F5
    F5 -->|Live Heritage Stats| P
```

---

## 6. Technology Stack Justification

| Layer | Chosen Technology | Rationale & Trade-offs |
| :--- | :--- | :--- |
| **Backend Framework** | **FastAPI (Python 3.11)** | Provides native asynchronous endpoints, automatic OpenAPI documentation, automatic validation via Pydantic, and exceptional execution speed comparable to NodeJS and Go. |
| **Validation Layer** | **Pydantic v2** | High-performance C-based `pydantic-core` parsing, strict schema enforcement, and declarative data typing. |
| **Server Engine** | **Uvicorn (ASGI)** | High-throughput asynchronous server supporting HTTP/1.1 and WebSockets. |
| **Template Engine** | **Jinja2** | Server-Side Rendering (SSR) gives instantaneous first-contentful paint without requiring heavy frontend JavaScript bundle downloads. |
| **Presentation Tier** | **Pure Modern CSS & Vanilla ES6** | Handloom-themed design system (Terracotta, Indigo, Raw Silk, Gold Zari) built with CSS custom properties and CSS Grid. Zero NPM or bundler dependencies required. |
| **Data Layer** | **Hybrid In-Memory + Seed JSON** | Zero-latency reads and writes with bootstrap seeding from `data/*.json`, enabling immediate evaluation and testing without complex database server setup. |
| **Test Suite** | **Pytest + HTTPX** | Deterministic unit and integration tests with automatic state isolation via fixtures. |

---

## 7. Security, Resilience & Quality Attributes

1. **Input Sanitization & Schema Validation:**
   - All inbound data payloads are strictly validated by Pydantic models with minimum/maximum length constraints, numerical bounds (e.g. `experience_years <= 80`, `loom_days <= 180`, `price_inr > 0`), and regex-based email validation.
2. **Fair-Trade Share Enforcement:**
   - Platform rules reject fair-trade artisan cuts below 70%, with a system default of 82% direct remittance.
3. **Inventory Race Condition Mitigation:**
   - In-memory order processing checks inventory and decrements atomically before order commitment.
4. **Offline Resilience:**
   - Email validation and core business logic run without external DNS queries or third-party web requests, ensuring dependable operation in sandboxed or air-gapped environments.

---

## 8. Extensibility & Future Scalability Roadmap

1. **Database Persistence Migration:**
   - Pluggable interface to transition `ThariDatabase` to **PostgreSQL** with SQLAlchemy 2.0 ORM and Alembic migrations.
2. **Automated Split Payments (UPI & Razorpay Route):**
   - Direct split disbursement at gateway level: 82% routed to Weaver's bank account, 5% to platform operations, and remainder to logistics.
3. **Weaver Voice & Multilingual Interface:**
   - Mobile PWA with voice recognition in regional languages (Hindi, Tamil, Telugu, Odia, Bengali) enabling non-literate weavers to dictate loom progress.
4. **Blockchain Provenance & NFC Weave Tags:**
   - Verification tags embedded into sari selvages linking to immutable on-chain proof of artisan identity, loom location, and GI authenticity.
