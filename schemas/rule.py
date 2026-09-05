"""Public API schemas for stored compliance rules and legacy validator exports."""

from datetime import date
from typing import Optional

from pydantic import BaseModel


class RuleResponse(BaseModel):
    id: int
    rule_id: str
    category: Optional[str] = None
    requirement: str
    description: Optional[str] = None
    mandatory: bool
    validation_type: Optional[str] = None
    severity: Optional[str] = None
    source: Optional[str] = None
    effective_date: Optional[date] = None

from backend.inspection.validator import (
    check_product_name,
    check_mrp,
    check_net_quantity,
    check_manufacturer,
    check_manufacturer_address,
    check_importer,
    check_importer_address,
    check_country_of_origin,
    check_customer_care,
    check_date,
    check_fssai_license,
    check_lot_batch,
    check_ingredients,
    check_nutrition,
    check_veg_nonveg_symbol,
    check_visual_review,
    check_not_automatable,
)

__all__ = [
    "check_product_name",
    "check_mrp",
    "check_net_quantity",
    "check_manufacturer",
    "check_manufacturer_address",
    "check_importer",
    "check_importer_address",
    "check_country_of_origin",
    "check_customer_care",
    "check_date",
    "check_fssai_license",
    "check_lot_batch",
    "check_ingredients",
    "check_nutrition",
    "check_veg_nonveg_symbol",
    "check_visual_review",
    "check_not_automatable",
]
