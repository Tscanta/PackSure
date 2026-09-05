"""Normalized rule-engine model, independent of database row shape."""

from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass(slots=True)
class Rule:
    # ``id`` is the numeric database primary key; ``rule_id`` is the legal reference.
    id: int | None
    rule_id: str
    category: str | None
    requirement: str
    description: str | None = None
    mandatory: bool = True
    validation_type: str | None = None
    severity: str | None = None
    source: str | None = None
    effective_date: date | None = None
    legal_reference: str | None = None
    applicability: str | None = None
    exceptions: str | None = None
    field: str | None = None
    operator: str | None = None
    value: Any = None

    @property
    def normalized_operator(self) -> str:
        return (self.operator or self.validation_type or "").strip().upper()

    def __getitem__(self, key: str) -> Any:
        """Mapping compatibility for the original repository callers."""
        return getattr(self, key)

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)
