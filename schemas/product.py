from pydantic import BaseModel, Field
from typing import Optional


class ProductCreate(BaseModel):
    product_name: str = Field(..., min_length=1)
    category: Optional[str] = None
    brand: Optional[str] = None
    manufacturer: Optional[str] = None


class ProductResponse(BaseModel):
    id: int
    product_name: str
    category: Optional[str]
    brand: Optional[str]
    manufacturer: Optional[str]
    created_at: Optional[str] = None