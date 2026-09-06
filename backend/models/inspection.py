"""Domain summary returned by a completed inspection."""

from dataclasses import dataclass, field
from typing import Any

from backend.models.violation import Violation


@dataclass(slots=True)
class InspectionResult:
    inspection_id: str
    overall_status: str
    score: float
    total_checks: int
    passed_checks: int
    failed_checks: int
    warning_checks: int
    checks: list[Any] = field(default_factory=list)
    violations: list[Violation] = field(default_factory=list)
    