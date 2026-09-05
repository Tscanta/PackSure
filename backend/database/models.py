from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional


# ============================================================
# PRODUCT
# ============================================================

@dataclass
class Product:
    id: Optional[int]
    product_name: str
    category: Optional[str]
    brand: Optional[str]
    manufacturer: Optional[str]
    created_at: Optional[datetime] = None


# ============================================================
# RULE
# ============================================================

@dataclass
class Rule:
    id: Optional[int]
    rule_id: str
    category: str
    requirement: str
    description: Optional[str]
    mandatory: bool
    validation_type: Optional[str]
    severity: Optional[str]
    source: Optional[str]
    effective_date: Optional[date]

    legal_reference: Optional[str]
    applicability: Optional[str]
    exceptions: Optional[str]

    created_at: Optional[datetime] = None


# ============================================================
# INSPECTION
# ============================================================

@dataclass
class Inspection:
    id: Optional[int]
    product_id: int
    inspection_date: Optional[datetime]
    overall_status: Optional[str]
    confidence: Optional[float]


# ============================================================
# VIOLATION
# ============================================================

@dataclass
class Violation:
    id: Optional[int]
    inspection_id: int
    rule_id: int
    status: str
    detected_value: Optional[str]
    expected_value: Optional[str]
    message: Optional[str]