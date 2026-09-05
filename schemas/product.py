from typing import Optional

from pydantic import BaseModel, Field


# ============================================================
# PRODUCT INPUT
# ============================================================

class ProductInput(BaseModel):
    """
    Structured product information extracted from a package.

    This model is the input to the compliance/rule engine.

    OCR / AI extraction
            ↓
        ProductInput
            ↓
        Rule Engine
            ↓
    Compliance Results
    """

    # ========================================================
    # BASIC PRODUCT INFORMATION
    # ========================================================

    product_name: Optional[str] = None

    product_category: Optional[str] = None

    brand: Optional[str] = None

    manufacturer: Optional[str] = None

    # ========================================================
    # MANUFACTURER / BRAND OWNER
    # ========================================================

    manufacturer_address: Optional[str] = None

    brand_owner: Optional[str] = None

    brand_owner_address: Optional[str] = None

    # Generic address fallback.
    # Some older extraction code may use this field.
    address: Optional[str] = None

    # ========================================================
    # IMPORT INFORMATION
    # ========================================================

    importer: Optional[str] = None

    importer_address: Optional[str] = None

    country_of_origin: Optional[str] = None

    # ========================================================
    # LEGAL METROLOGY
    # ========================================================

    mrp: Optional[str] = None

    net_quantity: Optional[str] = None

    dimensions: Optional[str] = None

    selling_price: Optional[str] = None

    # ========================================================
    # CUSTOMER CARE
    # ========================================================

    customer_care: Optional[str] = None

    customer_care_phone: Optional[str] = None

    customer_care_email: Optional[str] = None

    customer_care_address: Optional[str] = None

    # ========================================================
    # DATE / SHELF LIFE
    # ========================================================

    manufacturing_date: Optional[str] = None

    packaging_date: Optional[str] = None

    expiry_date: Optional[str] = None

    best_before: Optional[str] = None

    use_by: Optional[str] = None

    shelf_life: Optional[str] = None

    # ========================================================
    # LOT / BATCH
    # ========================================================

    lot_number: Optional[str] = None

    batch_number: Optional[str] = None

    lot_code: Optional[str] = None

    # ========================================================
    # FSSAI
    # ========================================================

    fssai_license_number: Optional[str] = None

    fssai_license_no: Optional[str] = None

    fssai_registration_number: Optional[str] = None

    # ========================================================
    # INGREDIENTS
    # ========================================================

    ingredients: Optional[str] = None

    ingredient_list: Optional[str] = None

    # ========================================================
    # NUTRITION
    # ========================================================

    nutrition: Optional[str] = None

    nutrition_facts: Optional[str] = None

    energy: Optional[str] = None

    protein: Optional[str] = None

    carbohydrate: Optional[str] = None

    total_sugars: Optional[str] = None

    added_sugars: Optional[str] = None

    total_fat: Optional[str] = None

    saturated_fat: Optional[str] = None

    trans_fat: Optional[str] = None

    cholesterol: Optional[str] = None

    sodium: Optional[str] = None

    dietary_fibre: Optional[str] = None

    # ========================================================
    # SERVING INFORMATION
    # ========================================================

    serving_size: Optional[str] = None

    servings_per_package: Optional[str] = None

    # ========================================================
    # VEG / NON-VEG
    # ========================================================

    veg_nonveg_symbol: Optional[str] = None

    food_symbol: Optional[str] = None

    vegetarian: Optional[bool] = None

    non_vegetarian: Optional[bool] = None

    # ========================================================
    # ALLERGEN INFORMATION
    # ========================================================

    allergens: Optional[str] = None

    contains_statement: Optional[str] = None

    may_contain_statement: Optional[str] = None

    # ========================================================
    # STORAGE / USAGE
    # ========================================================

    storage_instructions: Optional[str] = None

    instructions_for_use: Optional[str] = None

    preparation_instructions: Optional[str] = None

    # ========================================================
    # SPECIAL DECLARATIONS
    # ========================================================

    warnings: Optional[str] = None

    declarations: Optional[str] = None

    additives: Optional[str] = None

    flavouring: Optional[str] = None

    # ========================================================
    # PRODUCT TYPE / SPECIAL CATEGORY
    # ========================================================

    food_type: Optional[str] = None

    product_type: Optional[str] = None

    is_imported: Optional[bool] = None

    is_non_retail: Optional[bool] = None

    is_single_ingredient: Optional[bool] = None

    # ========================================================
    # PACKAGING INFORMATION
    # ========================================================

    package_type: Optional[str] = None

    package_size: Optional[str] = None

    ppp_area: Optional[str] = None

    principal_display_panel: Optional[str] = None

    # ========================================================
    # RAW OCR
    # ========================================================

    raw_text: Optional[str] = None

    # ========================================================
    # OCR CONFIDENCE
    # ========================================================

    ocr_confidence: Optional[float] = Field(
        default=None,
        ge=0,
        le=100
    )


# ============================================================
# PRODUCT RESPONSE
# ============================================================

class ProductResponse(ProductInput):
    """
    Product returned by the API.
    """

    id: Optional[int] = None


# ============================================================
# PRODUCT CREATION REQUEST
# ============================================================

class ProductCreate(ProductInput):
    """
    Payload used when creating a product.
    """

    pass


# ============================================================
# PRODUCT UPDATE REQUEST
# ============================================================

class ProductUpdate(BaseModel):
    """
    Payload used when partially updating a product.

    All fields are optional.
    """

    product_name: Optional[str] = None

    product_category: Optional[str] = None

    brand: Optional[str] = None

    manufacturer: Optional[str] = None

    manufacturer_address: Optional[str] = None

    brand_owner: Optional[str] = None

    brand_owner_address: Optional[str] = None

    address: Optional[str] = None

    importer: Optional[str] = None

    importer_address: Optional[str] = None

    country_of_origin: Optional[str] = None

    mrp: Optional[str] = None

    net_quantity: Optional[str] = None

    dimensions: Optional[str] = None

    selling_price: Optional[str] = None

    customer_care: Optional[str] = None

    customer_care_phone: Optional[str] = None

    customer_care_email: Optional[str] = None

    customer_care_address: Optional[str] = None

    manufacturing_date: Optional[str] = None

    packaging_date: Optional[str] = None

    expiry_date: Optional[str] = None

    best_before: Optional[str] = None

    use_by: Optional[str] = None

    shelf_life: Optional[str] = None

    lot_number: Optional[str] = None

    batch_number: Optional[str] = None

    lot_code: Optional[str] = None

    fssai_license_number: Optional[str] = None

    fssai_license_no: Optional[str] = None

    fssai_registration_number: Optional[str] = None

    ingredients: Optional[str] = None

    ingredient_list: Optional[str] = None

    nutrition: Optional[str] = None

    nutrition_facts: Optional[str] = None

    energy: Optional[str] = None

    protein: Optional[str] = None

    carbohydrate: Optional[str] = None

    total_sugars: Optional[str] = None

    added_sugars: Optional[str] = None

    total_fat: Optional[str] = None

    saturated_fat: Optional[str] = None

    trans_fat: Optional[str] = None

    cholesterol: Optional[str] = None

    sodium: Optional[str] = None

    dietary_fibre: Optional[str] = None

    serving_size: Optional[str] = None

    servings_per_package: Optional[str] = None

    veg_nonveg_symbol: Optional[str] = None

    food_symbol: Optional[str] = None

    vegetarian: Optional[bool] = None

    non_vegetarian: Optional[bool] = None

    allergens: Optional[str] = None

    contains_statement: Optional[str] = None

    may_contain_statement: Optional[str] = None

    storage_instructions: Optional[str] = None

    instructions_for_use: Optional[str] = None

    preparation_instructions: Optional[str] = None

    warnings: Optional[str] = None

    declarations: Optional[str] = None

    additives: Optional[str] = None

    flavouring: Optional[str] = None

    food_type: Optional[str] = None

    product_type: Optional[str] = None

    is_imported: Optional[bool] = None

    is_non_retail: Optional[bool] = None

    is_single_ingredient: Optional[bool] = None

    package_type: Optional[str] = None

    package_size: Optional[str] = None

    ppp_area: Optional[str] = None

    principal_display_panel: Optional[str] = None

    raw_text: Optional[str] = None

    ocr_confidence: Optional[float] = Field(
        default=None,
        ge=0,
        le=100
    )

# ============================================================
# PRODUCT
# ============================================================

class Product(ProductInput):
    """
    Complete product model used by the extraction pipeline.

    Product extends ProductInput so that existing extraction
    code can continue using:

        from schemas.product import Product

    while the inspection system can use the same fields.
    """

    id: Optional[int] = None