"""Structured explanation for a failed deterministic rule check."""

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Violation:
    field: str
    rule_id: str
    message: str
    expected_value: Any = None
    actual_value: Any = None
    severity: str | None = None
    database_rule_id: int | None = None
