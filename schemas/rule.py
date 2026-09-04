from pydantic import BaseModel
from typing import Optional


class RuleResponse(BaseModel):
    id: int
    rule_id: str
    category: str
    requirement: str
    description: Optional[str]
    mandatory: bool
    validation_type: Optional[str]
    severity: Optional[str]
    source: Optional[str]
    effective_date: Optional[str]
    created_at: Optional[str]