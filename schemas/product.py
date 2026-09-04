from pydantic import BaseModel
from typing import Optional


# ============================================================
# PRODUCT INPUT
# Used by the inspection engine
# ============================================================

class ProductInput(BaseModel):
    product_name: Optional[str] = None
    brand: Optional[str] = None

    mrp: Optional[str] = None
    net_quantity: Optional[str] = None

    manufacturer: Optional[str] = None
    manufacturer_address: Optional[str] = None

    importer: Optional[str] = None
    importer_address: Optional[str] = None

    country_of_origin: Optional[str] = None

    customer_care: Optional[str] = None

    manufacturing_date: Optional[str] = None
    expiry_date: Optional[str] = None

    raw_text: Optional[str] = None


# ============================================================
# PRODUCT CREATE
# Used when manually creating a product
# ============================================================

class ProductCreate(BaseModel):
    product_name: str
    category: str
    brand: Optional[str] = None
    manufacturer: Optional[str] = None


# ============================================================
# PRODUCT RESPONSE
# Returned by the API
# ============================================================

class ProductResponse(BaseModel):
    id: int
    product_name: str
    category: str
    brand: Optional[str] = None
    manufacturer: Optional[str] = None

    class Config:
        from_attributes = True