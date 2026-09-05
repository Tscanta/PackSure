from typing import Optional, Literal

from pydantic import BaseModel, Field
from backend.models.violation import Violation


CheckStatus = Literal[
    "PASS",
    "FAIL",
    "WARNING",
    "REVIEW",
    "NOT_APPLICABLE",
]

OverallStatus = Literal[
    "COMPLIANT",
    "NON_COMPLIANT",
    "REVIEW_REQUIRED",
]


class CheckResult(BaseModel):
    field: str

    status: CheckStatus

    message: str

    rule_id: Optional[str] = None

    severity: Optional[str] = None

    mandatory: bool = False

    detected_value: Optional[str] = None

    expected_value: Optional[str] = None

    confidence: Optional[float] = Field(
        default=None,
        ge=0,
        le=100,
    )

    evidence: Optional[str] = None

    database_rule_id: Optional[int] = None


class InspectionResult(BaseModel):
    inspection_id: str

    overall_status: OverallStatus

    score: float = Field(
        default=0,
        ge=0,
        le=100,
    )

    total_checks: int = 0

    passed_checks: int = 0

    failed_checks: int = 0

    warning_checks: int = 0

    review_checks: int = 0

    checks: list[CheckResult] = Field(
        default_factory=list
    )

    violations: list[Violation] = Field(default_factory=list)
