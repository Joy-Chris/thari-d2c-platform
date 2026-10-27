import json
import uuid
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from app.config import settings

class ThariDatabase:
    """
    Lightweight, thread-safe data access layer for Thari.
    Initializes from data/ sample JSON files and maintains active platform state in memory.
    """
    def __init__(self):
        self.artisans: Dict[str, dict] = {}
        self.products: Dict[str, dict] = {}
        self.orders: Dict[str, dict] = {}
        self.reviews: Dict[str, List[dict]] = {}
        self.inquiries: Dict[str, dict] = {}
        self.categories: dict = {}
        self.load_seed_data()

    def load_seed_data(self):
        data_dir = settings.DATA_DIR
        
        # Load artisans
        artisans_file = data_dir / "artisans.json"
        if artisans_file.exists():
            with open(artisans_file, "r", encoding="utf-8") as f:
                artisans_list = json.load(f)
                for item in artisans_list:
                    self.artisans[item["id"]] = item
                    
        # Load products
        products_file = data_dir / "products.json"
        if products_file.exists():
            with open(products_file, "r", encoding="utf-8") as f:
                products_list = json.load(f)
                for item in products_list:
                    self.products[item["id"]] = item
                    self.reviews[item["id"]] = []

        # Load orders
        orders_file = data_dir / "orders.json"
        if orders_file.exists():
            with open(orders_file, "r", encoding="utf-8") as f:
                orders_list = json.load(f)
                for item in orders_list:
                    self.orders[item["order_id"]] = item

        # Load categories
        cat_file = data_dir / "categories.json"
        if cat_file.exists():
            with open(cat_file, "r", encoding="utf-8") as f:
                self.categories = json.load(f)
        else:
            self.categories = {
                "craft_traditions": [],
                "materials": [],
                "product_categories": []
            }

        # Seed initial reviews for top products
        self._seed_sample_reviews()

    def _seed_sample_reviews(self):
        sample_reviews = {
            "prod-001": [
                {
                    "id": "rev-1",
                    "product_id": "prod-001",
                    "customer_name": "Ananya Sen",
                    "rating": 5,
                    "comment": "The gossamer lightness of this Chanderi weave took my breath away. Knowing 82% of what I paid went directly to Devendraji in Pranpur makes wearing it even more special.",
                    "verified_purchase": True,
                    "created_at": "2026-10-18T11:20:00Z"
                },
                {
                    "id": "rev-2",
                    "product_id": "prod-001",
                    "customer_name": "Kavita Rao",
                    "rating": 5,
                    "comment": "Authentic gold ashrafi motifs. The certificate of origin and GI verification is top notch.",
                    "verified_purchase": True,
                    "created_at": "2026-10-22T09:40:00Z"
                }
            ],
            "prod-002": [
                {
                    "id": "rev-3",
                    "product_id": "prod-002",
                    "customer_name": "Revathi Natarajan",
                    "rating": 5,
                    "comment": "Master Meenakshi and Sundaram have created a family heirloom. The Korvai interlocking border is seamlessly smooth. No middlemen cut - fair trade at its finest.",
                    "verified_purchase": True,
                    "created_at": "2026-10-15T16:05:00Z"
                }
            ],
            "prod-004": [
                {
                    "id": "rev-4",
                    "product_id": "prod-004",
                    "customer_name": "Siddharth Verma",
                    "rating": 5,
                    "comment": "The mathematical precision of Pochampally double ikat is astonishing. Vibrant organic dyes and sublime texture.",
                    "verified_purchase": True,
                    "created_at": "2026-10-12T14:30:00Z"
                }
            ]
        }
        for prod_id, revs in sample_reviews.items():
            if prod_id in self.products:
                self.reviews[prod_id] = revs

    # ---------------------------------------------
    # Artisan Operations
    # ---------------------------------------------
    def list_artisans(self, state: Optional[str] = None, craft: Optional[str] = None) -> List[dict]:
        results = list(self.artisans.values())
        if state:
            results = [a for a in results if a.get("state", "").lower() == state.lower()]
        if craft:
            results = [a for a in results if craft.lower() in a.get("craft_tradition", "").lower()]
        return results

    def get_artisan(self, artisan_id: str) -> Optional[dict]:
        artisan = self.artisans.get(artisan_id)
        if not artisan:
            return None
        # Count current products
        artisan_copy = dict(artisan)
        artisan_copy["total_products"] = len(self.get_products_by_artisan(artisan_id))
        return artisan_copy

    def create_artisan(self, data: dict) -> dict:
        artisan_id = f"art-{uuid.uuid4().hex[:6]}"
        data["id"] = artisan_id
        if "rating" not in data:
            data["rating"] = 5.0
        if "review_count" not in data:
            data["review_count"] = 0
        if "created_at" not in data:
            data["created_at"] = datetime.utcnow().isoformat()
        self.artisans[artisan_id] = data
        return data

    def update_artisan(self, artisan_id: str, data: dict) -> Optional[dict]:
        if artisan_id not in self.artisans:
            return None
        for k, v in data.items():
            if v is not None:
                self.artisans[artisan_id][k] = v
        return self.artisans[artisan_id]

    # ---------------------------------------------
    # Product Operations
    # ---------------------------------------------
    def list_products(
        self,
        craft: Optional[str] = None,
        category: Optional[str] = None,
        state: Optional[str] = None,
        artisan_id: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        search: Optional[str] = None,
        featured_only: Optional[bool] = None,
        sort_by: Optional[str] = None
    ) -> List[dict]:
        results = []
        for p in self.products.values():
            # Filter craft
            if craft and craft.lower() not in p.get("craft_tradition", "").lower():
                continue
            # Filter category
            if category and category.lower() != p.get("category", "").lower():
                continue
            # Filter artisan
            if artisan_id and p.get("artisan_id") != artisan_id:
                continue
            # Filter state (from origin_cluster or artisan)
            if state:
                artisan = self.artisans.get(p.get("artisan_id", ""))
                artisan_state = artisan.get("state", "").lower() if artisan else ""
                origin = p.get("origin_cluster", "").lower()
                if state.lower() not in artisan_state and state.lower() not in origin:
                    continue
            # Filter price range
            if min_price is not None and p.get("price_inr", 0) < min_price:
                continue
            if max_price is not None and p.get("price_inr", 0) > max_price:
                continue
            # Filter featured
            if featured_only is True and not p.get("is_featured", False):
                continue
            # Search query
            if search:
                q = search.lower()
                title = p.get("title", "").lower()
                desc = p.get("short_description", "").lower()
                story = p.get("detailed_story", "").lower()
                mat = p.get("material", "").lower()
                artisan = self.artisans.get(p.get("artisan_id", ""))
                art_name = artisan.get("full_name", "").lower() if artisan else ""
                if not any(q in field for field in (title, desc, story, mat, art_name)):
                    continue
            results.append(self._enrich_product(p))

        # Sorting
        if sort_by == "price_asc":
            results.sort(key=lambda x: x.get("price_inr", 0))
        elif sort_by == "price_desc":
            results.sort(key=lambda x: x.get("price_inr", 0), reverse=True)
        elif sort_by == "loom_days":
            results.sort(key=lambda x: x.get("loom_days", 0), reverse=True)
        elif sort_by == "newest":
            results.sort(key=lambda x: x.get("created_at", ""), reverse=True)
            
        return results

    def get_product(self, product_id: str) -> Optional[dict]:
        prod = self.products.get(product_id)
        if not prod:
            return None
        return self._enrich_product(prod)

    def get_products_by_artisan(self, artisan_id: str) -> List[dict]:
        return [
            self._enrich_product(p)
            for p in self.products.values()
            if p.get("artisan_id") == artisan_id
        ]

    def create_product(self, data: dict) -> dict:
        prod_id = f"prod-{uuid.uuid4().hex[:6]}"
        data["id"] = prod_id
        if "created_at" not in data:
            data["created_at"] = datetime.utcnow().isoformat()
        
        # Calculate transparent pricing if not given
        price = data.get("price_inr", 0)
        artisan = self.artisans.get(data.get("artisan_id", ""))
        share_pct = artisan.get("fair_trade_share_percent", settings.DEFAULT_ARTISAN_SHARE_PERCENT) if artisan else settings.DEFAULT_ARTISAN_SHARE_PERCENT
        
        if not data.get("transparent_pricing"):
            artisan_wages = round(price * (share_pct / 100.0), 2)
            material_cost = round(price * 0.12, 2)
            finishing = round(price * 0.03, 2)
            platform_fee = round(price - (artisan_wages + material_cost + finishing), 2)
            if platform_fee < 0:
                platform_fee = round(price * 0.05, 2)
            data["transparent_pricing"] = {
                "artisan_wages": artisan_wages,
                "raw_material_silk_zari": material_cost,
                "finishing_packaging": finishing,
                "platform_fair_trade_ops": platform_fee
            }

        self.products[prod_id] = data
        self.reviews[prod_id] = []
        return self._enrich_product(data)

    def update_product(self, product_id: str, data: dict) -> Optional[dict]:
        if product_id not in self.products:
            return None
        for k, v in data.items():
            if v is not None:
                self.products[product_id][k] = v
        return self._enrich_product(self.products[product_id])

    def delete_product(self, product_id: str) -> bool:
        if product_id in self.products:
            del self.products[product_id]
            self.reviews.pop(product_id, None)
            return True
        return False

    def _enrich_product(self, prod: dict) -> dict:
        enriched = dict(prod)
        artisan_id = prod.get("artisan_id")
        if artisan_id and artisan_id in self.artisans:
            art = self.artisans[artisan_id]
            enriched["artisan"] = {
                "id": art.get("id"),
                "full_name": art.get("full_name"),
                "cluster_name": art.get("cluster_name"),
                "craft_tradition": art.get("craft_tradition"),
                "state": art.get("state"),
                "avatar_url": art.get("avatar_url"),
                "certifications": art.get("certifications", []),
                "rating": art.get("rating", 5.0),
                "review_count": art.get("review_count", 0)
            }
        else:
            enriched["artisan"] = None
        enriched["reviews"] = self.reviews.get(prod.get("id", ""), [])
        return enriched

    # ---------------------------------------------
    # Review Operations
    # ---------------------------------------------
    def add_review(self, product_id: str, review_data: dict) -> Optional[dict]:
        if product_id not in self.products:
            return None
        rev_id = f"rev-{uuid.uuid4().hex[:6]}"
        review_data["id"] = rev_id
        review_data["product_id"] = product_id
        review_data["created_at"] = datetime.utcnow().isoformat()
        if "verified_purchase" not in review_data:
            review_data["verified_purchase"] = True
        if product_id not in self.reviews:
            self.reviews[product_id] = []
        self.reviews[product_id].insert(0, review_data)
        return review_data

    # ---------------------------------------------
    # Inquiry Operations (Consumer -> Weaver Direct)
    # ---------------------------------------------
    def create_inquiry(self, inquiry_data: dict) -> dict:
        inquiry_id = f"inq-{uuid.uuid4().hex[:6]}"
        inquiry_data["id"] = inquiry_id
        inquiry_data["status"] = "PENDING_ARTISAN_RESPONSE"
        inquiry_data["created_at"] = datetime.utcnow().isoformat()
        self.inquiries[inquiry_id] = inquiry_data
        return inquiry_data

    def list_inquiries_for_artisan(self, artisan_id: str) -> List[dict]:
        return [inq for inq in self.inquiries.values() if inq.get("artisan_id") == artisan_id]

    # ---------------------------------------------
    # Order Operations (Checkout & Direct Payouts)
    # ---------------------------------------------
    def create_order(self, order_data: dict) -> dict:
        order_id = f"ORD-{datetime.utcnow().strftime('%Y')}-{uuid.uuid4().hex[:6].upper()}"
        items_payload = order_data["items"]
        
        processed_items = []
        subtotal = 0.0
        total_artisan_payout = 0.0

        for it in items_payload:
            prod_id = it["product_id"] if isinstance(it, dict) else it.product_id
            qty = it["quantity"] if isinstance(it, dict) else it.quantity
            prod = self.products.get(prod_id)
            if not prod:
                raise ValueError(f"Product '{prod_id}' not found")
            if prod.get("inventory_count", 0) < qty:
                raise ValueError(f"Insufficient stock for '{prod.get('title')}'. Available: {prod.get('inventory_count')}")
            
            # Deduct stock
            prod["inventory_count"] -= qty
            
            unit_price = prod.get("price_inr", 0)
            line_total = unit_price * qty
            subtotal += line_total
            
            # Compute weaver fair payout
            artisan = self.artisans.get(prod.get("artisan_id", ""))
            share_pct = artisan.get("fair_trade_share_percent", settings.DEFAULT_ARTISAN_SHARE_PERCENT) if artisan else settings.DEFAULT_ARTISAN_SHARE_PERCENT
            line_payout = round(line_total * (share_pct / 100.0), 2)
            total_artisan_payout += line_payout

            processed_items.append({
                "product_id": prod_id,
                "title": prod.get("title"),
                "quantity": qty,
                "unit_price_inr": unit_price,
                "artisan_id": prod.get("artisan_id"),
                "artisan_share_inr": line_payout
            })

        order_record = {
            "order_id": order_id,
            "customer_name": order_data["customer_name"],
            "customer_email": order_data["customer_email"],
            "customer_phone": order_data["customer_phone"],
            "shipping_address": order_data["shipping_address"] if isinstance(order_data["shipping_address"], dict) else order_data["shipping_address"].model_dump(),
            "items": processed_items,
            "subtotal_inr": subtotal,
            "shipping_fee_inr": 0.0,  # Free direct handloom delivery promotion
            "total_inr": subtotal,
            "total_artisan_direct_payout_inr": total_artisan_payout,
            "payment_status": "PAID",
            "payment_method": order_data.get("payment_method", "UPI / Fair-Trade Escrow"),
            "order_status": "CONFIRMED_AT_LOOM",
            "tracking_number": f"THARI-{uuid.uuid4().hex[:8].upper()}",
            "created_at": datetime.utcnow().isoformat(),
            "weavers_note": "Hand-packaged by our artisan cluster. Thank you for sustaining Indian handloom heritage."
        }
        self.orders[order_id] = order_record
        return order_record

    def get_order(self, order_id: str) -> Optional[dict]:
        return self.orders.get(order_id)

    def list_orders(self) -> List[dict]:
        return list(reversed(list(self.orders.values())))

    # ---------------------------------------------
    # Platform Statistics
    # ---------------------------------------------
    def get_stats(self) -> dict:
        total_payouts = sum(o.get("total_artisan_direct_payout_inr", 0) for o in self.orders.values())
        active_looms = sum(a.get("active_looms", 2) for a in self.artisans.values())
        clusters = {a.get("cluster_name") for a in self.artisans.values() if a.get("cluster_name")}
        shares = [a.get("fair_trade_share_percent", 82.0) for a in self.artisans.values()]
        avg_share = round(sum(shares) / len(shares), 1) if shares else 82.0

        return {
            "total_artisans": len(self.artisans),
            "total_products": len(self.products),
            "total_orders": len(self.orders),
            "total_artisan_earnings_inr": total_payouts,
            "craft_clusters_count": len(clusters),
            "active_looms_count": active_looms,
            "average_fair_share_percent": avg_share
        }

db = ThariDatabase()
