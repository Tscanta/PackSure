from pydantic import BaseModel
from typing import Optional


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


class Product(BaseModel):
    product_name: Optional[str] = None
    product_category: Optional[str] = None

    mrp: Optional[float] = None
    net_quantity: Optional[str] = None

    manufacturer: Optional[str] = None
    manufacturer_address: Optional[str] = None

    importer: Optional[str] = None
    country_of_origin: Optional[str] = None

    ingredients: Optional[str] = None
    allergens: Optional[str] = None

    best_before: Optional[str] = None

    fssai_license: Optional[str] = None
    customer_care: Optional[str] = None

    nutrition: Optional[Nutrition] = None

    raw_text: Optional[str] = None