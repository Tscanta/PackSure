from datetime import date

from pydantic import BaseModel


class Rule(BaseModel):
    rule_id: str
    category: str
    requirement: str
    description: str | None = None
    mandatory: bool
    validation_type: str
    severity: str
    source: str
    effective_date: date