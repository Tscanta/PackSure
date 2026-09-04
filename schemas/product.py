from typing import Optional

from pydantic import BaseModel, ConfigDict


# ============================================================
# NUTRITION
# Used by OCR / extraction pipeline
# ============================================================

class Nutrition(BaseModel):
    serving_size: Optional[str] = None

    calories: Optional[float] = None
    total_fat: Optional[float] = None
    saturated_fat: Optional[float] = None
    trans_fat: Optional[float] = None
    cholesterol: Optional[float] = None
    sodium: Optional[float] = None
    potassium: Optional[float] = None

    total_carbohydrate: Optional[float] = None
    dietary_fiber: Optional[float] = None
    sugars: Optional[float] = None
    protein: Optional[float] = None

    vitamin_a: Optional[float] = None
    vitamin_c: Optional[float] = None
    vitamin_d: Optional[float] = None

    calcium: Optional[float] = None
    iron: Optional[float] = None
    magnesium: Optional[float] = None
    phosphorus: Optional[float] = None
    niacin: Optional[float] = None
    vitamin_b6: Optional[float] = None


# ============================================================
# EXTRACTED PRODUCT
# Produced by OCR + parser
#
# This is the main structured representation produced
# by the extraction pipeline.
# ============================================================

class Product(BaseModel):
    # --------------------------------------------------------
    # Basic product information
    # --------------------------------------------------------

    product_name: Optional[str] = None
    product_category: Optional[str] = None

    # --------------------------------------------------------
    # Price / quantity
    # --------------------------------------------------------

    mrp: Optional[float] = None
    net_quantity: Optional[str] = None

    # --------------------------------------------------------
    # Manufacturer
    # --------------------------------------------------------

    manufacturer: Optional[str] = None
    manufacturer_address: Optional[str] = None

    # --------------------------------------------------------
    # Importer / marketer
    # --------------------------------------------------------

    importer: Optional[str] = None
    importer_address: Optional[str] = None

    # --------------------------------------------------------
    # Origin
    # --------------------------------------------------------

    country_of_origin: Optional[str] = None

    # --------------------------------------------------------
    # Ingredients / allergens
    # --------------------------------------------------------

    ingredients: Optional[str] = None
    allergens: Optional[str] = None

    # --------------------------------------------------------
    # Dates
    # --------------------------------------------------------

    manufacturing_date: Optional[str] = None
    best_before: Optional[str] = None

    # --------------------------------------------------------
    # Regulatory / contact information
    # --------------------------------------------------------

    fssai_license: Optional[str] = None
    customer_care: Optional[str] = None

    # --------------------------------------------------------
    # Nutrition
    # --------------------------------------------------------

    nutrition: Optional[Nutrition] = None

    # --------------------------------------------------------
    # Original OCR text
    # --------------------------------------------------------

    raw_text: Optional[str] = None


# ============================================================
# PRODUCT INPUT
# Used by the inspection / compliance engine
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
# Used when creating a product in the database
# ============================================================

class ProductCreate(BaseModel):
    product_name: str
    category: str
    brand: Optional[str] = None
    manufacturer: Optional[str] = None


# ============================================================
# PRODUCT RESPONSE
# Used for API / database responses
# ============================================================

class ProductResponse(BaseModel):
    id: int
    product_name: str
    category: str
    brand: Optional[str] = None
    manufacturer: Optional[str] = None

    # Pydantic V2 replacement for:
    #
    # class Config:
    #     from_attributes = True
    #
    model_config = ConfigDict(from_attributes=True)