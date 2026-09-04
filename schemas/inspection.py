from pydantic import BaseModel
from typing import Optional, List


class CheckResult(BaseModel):
    field: str
    status: str
    message: str
    rule_id: Optional[str] = None
    severity: Optional[str] = None
    mandatory: Optional[bool] = None


class InspectionResult(BaseModel):
    inspection_id: str
    overall_status: str
    score: float
    total_checks: int
    passed_checks: int
    failed_checks: int
    warning_checks: int
    checks: List[CheckResult]


class InspectionCreate(BaseModel):
    product_id: int
    overall_status: str
    confidence: float


class InspectionResponse(BaseModel):
    id: int
    product_id: int
    inspection_date: Optional[str] = None
    overall_status: str
    confidence: Optional[float] = None