from pydantic import BaseModel
from typing import Optional


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