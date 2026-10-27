from typing import Optional, List, Annotated
from pydantic import BaseModel, Field
from datetime import datetime

# Regex pattern for email validation without DNS deliverability checks
EmailPattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
EmailType = Annotated[str, Field(pattern=EmailPattern, description="Email address")]

# ==========================================
# Artisan Schemas
# ==========================================

class ArtisanBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=120, description="Artisan master weaver name")
    cluster_name: str = Field(..., min_length=2, max_length=150, description="Weaver guild, cooperative or self-help group")
    craft_tradition: str = Field(..., description="e.g. Chanderi, Kanchipuram Korvai, Pochampally Ikat, Jamdani Muslin")
    loom_type: str = Field(..., description="e.g. Pit Loom, Frame Loom, Three-Shuttle Korvai Loom, Dobby")
    village: str = Field(..., description="Village or hamlet of weaving cluster")
    district: str = Field(..., description="District")
    state: str = Field(..., description="Indian State")
    experience_years: int = Field(..., ge=0, le=80, description="Years engaged in traditional handloom weaving")
    bio: str = Field(..., min_length=20, description="Artisan personal story, heritage background and craft lineage")
    phone: str = Field(..., description="Contact number for direct communication")
    email: EmailType = Field(..., description="Email address for notifications and order settlements")
    certifications: List[str] = Field(default_factory=list, description="GI tag certification, Handloom Mark, Craftmark")
    fair_trade_share_percent: float = Field(default=82.0, ge=70.0, le=95.0, description="Guaranteed % of price paid directly to weaver")
    avatar_url: Optional[str] = Field(default="https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=600&q=80")
    hero_image_url: Optional[str] = Field(default="https://images.unsplash.com/photo-1607344645866-009c320b5ab8?auto=format&fit=crop&w=1200&q=80")
    active_looms: int = Field(default=2, ge=1, le=50, description="Number of operational handlooms in workshop")

class ArtisanCreate(ArtisanBase):
    pass

class ArtisanUpdate(BaseModel):
    full_name: Optional[str] = None
    cluster_name: Optional[str] = None
    craft_tradition: Optional[str] = None
    loom_type: Optional[str] = None
    village: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    experience_years: Optional[int] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailType] = None
    certifications: Optional[List[str]] = None
    fair_trade_share_percent: Optional[float] = None
    avatar_url: Optional[str] = None
    hero_image_url: Optional[str] = None
    active_looms: Optional[int] = None

class ArtisanSummary(BaseModel):
    id: str
    full_name: str
    cluster_name: str
    craft_tradition: str
    state: str
    avatar_url: Optional[str] = None
    certifications: List[str] = []
    rating: float = 5.0
    review_count: int = 0

class ArtisanResponse(ArtisanBase):
    id: str
    rating: float = 5.0
    review_count: int = 0
    total_products: int = 0
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


# ==========================================
# Product Schemas
# ==========================================

class TransparentPricing(BaseModel):
    artisan_wages: float = Field(..., ge=0, description="Direct cash compensation to weaver for handloom labor")
    raw_material_silk_zari: float = Field(..., ge=0, description="Cost of pure silk, organic cotton, silver-gold zari")
    finishing_packaging: float = Field(default=250.0, ge=0, description="Washing, edge stitching, artisanal box")
    platform_fair_trade_ops: float = Field(default=350.0, ge=0, description="Quality check, logistics, escrow insurance")

class ProductBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=200, description="Title of the handloom textile")
    artisan_id: str = Field(..., description="ID of registered artisan weaver")
    craft_tradition: str = Field(..., description="Weaving tradition e.g. Chanderi, Kanchipuram, Sambalpuri")
    category: str = Field(..., description="Sarees, Dupattas & Stoles, Unstitched Fabric & Yardage, etc.")
    material: str = Field(..., description="Fibers e.g. 100% Mulberry Silk, Khadi Cotton 100s, Tussar Silk")
    warp_yarn: Optional[str] = Field(default="Mulberry Silk 20/22D", description="Warp yarn technical specification")
    weft_yarn: Optional[str] = Field(default="Combed Cotton 100s", description="Weft yarn technical specification")
    loom_type: Optional[str] = Field(default="Traditional Pit Loom", description="Handloom mechanism used")
    loom_days: int = Field(..., ge=1, le=180, description="Total days required to weave one piece by hand")
    dimensions: str = Field(..., description="Dimensions (e.g. 6.3m x 1.15m or 2.5m x 0.9m)")
    color: str = Field(..., description="Color palette and aesthetic description")
    dye_type: Optional[str] = Field(default="Natural & Azo-Free Eco Dyes", description="Dyeing method")
    gi_tag_certified: bool = Field(default=True, description="GI tag authenticity status")
    handloom_mark: bool = Field(default=True, description="Handloom Mark verified")
    price_inr: float = Field(..., gt=0, description="Retail price in INR")
    inventory_count: int = Field(default=1, ge=0, description="Available handwoven inventory")
    short_description: str = Field(..., min_length=15, max_length=300)
    detailed_story: str = Field(..., min_length=50, description="The cultural story, loom technique, and weaver narrative")
    transparent_pricing: Optional[TransparentPricing] = None
    images: List[str] = Field(default_factory=list, description="High-resolution image URLs")
    is_featured: bool = Field(default=False)
    care_instructions: Optional[str] = Field(default="Dry clean recommended or gentle cold handwash.")
    origin_cluster: Optional[str] = Field(default="India")

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    title: Optional[str] = None
    craft_tradition: Optional[str] = None
    category: Optional[str] = None
    material: Optional[str] = None
    warp_yarn: Optional[str] = None
    weft_yarn: Optional[str] = None
    loom_type: Optional[str] = None
    loom_days: Optional[int] = None
    dimensions: Optional[str] = None
    color: Optional[str] = None
    dye_type: Optional[str] = None
    gi_tag_certified: Optional[bool] = None
    handloom_mark: Optional[bool] = None
    price_inr: Optional[float] = None
    inventory_count: Optional[int] = None
    short_description: Optional[str] = None
    detailed_story: Optional[str] = None
    transparent_pricing: Optional[TransparentPricing] = None
    images: Optional[List[str]] = None
    is_featured: Optional[bool] = None
    care_instructions: Optional[str] = None
    origin_cluster: Optional[str] = None

class ReviewItem(BaseModel):
    id: str
    product_id: str
    customer_name: str
    rating: int = Field(..., ge=1, le=5)
    comment: str
    verified_purchase: bool = True
    created_at: str

class ProductResponse(ProductBase):
    id: str
    artisan: Optional[ArtisanSummary] = None
    reviews: List[ReviewItem] = []
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


# ==========================================
# Review Schemas
# ==========================================

class ReviewCreate(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=100)
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(..., min_length=5, max_length=1000)


# ==========================================
# Inquiry Schemas (Direct Weaver Messaging)
# ==========================================

class InquiryCreate(BaseModel):
    product_id: Optional[str] = None
    artisan_id: str = Field(..., description="Artisan being contacted")
    customer_name: str = Field(..., min_length=2, max_length=100)
    customer_email: EmailType
    customer_phone: Optional[str] = None
    message: str = Field(..., min_length=10, max_length=2000, description="Message or bespoke weaving query")
    custom_dimensions_requested: Optional[str] = None

class InquiryResponse(InquiryCreate):
    id: str
    status: str = "PENDING_ARTISAN_RESPONSE"
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


# ==========================================
# Order Schemas
# ==========================================

class ShippingAddress(BaseModel):
    street: str = Field(..., min_length=5)
    city: str = Field(..., min_length=2)
    state: str = Field(..., min_length=2)
    pincode: str = Field(..., min_length=4, max_length=10)
    country: str = "India"

class OrderItemCreate(BaseModel):
    product_id: str
    quantity: int = Field(default=1, ge=1, le=10)

class OrderItemResponse(BaseModel):
    product_id: str
    title: str
    quantity: int
    unit_price_inr: float
    artisan_id: str
    artisan_share_inr: float

class OrderCreate(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=120)
    customer_email: EmailType
    customer_phone: str = Field(..., min_length=8, max_length=18)
    shipping_address: ShippingAddress
    items: List[OrderItemCreate] = Field(..., min_length=1)
    payment_method: str = Field(default="UPI / Fair-Trade Escrow")
    special_instructions: Optional[str] = None

class OrderResponse(BaseModel):
    order_id: str
    customer_name: str
    customer_email: str
    customer_phone: str
    shipping_address: ShippingAddress
    items: List[OrderItemResponse]
    subtotal_inr: float
    shipping_fee_inr: float = 0.0
    total_inr: float
    total_artisan_direct_payout_inr: float
    payment_status: str
    payment_method: str
    order_status: str
    tracking_number: Optional[str] = None
    created_at: str
    weavers_note: Optional[str] = None


# ==========================================
# Stats & Metadata Schemas
# ==========================================

class PlatformStats(BaseModel):
    total_artisans: int
    total_products: int
    total_orders: int
    total_artisan_earnings_inr: float
    craft_clusters_count: int
    active_looms_count: int
    average_fair_share_percent: float
