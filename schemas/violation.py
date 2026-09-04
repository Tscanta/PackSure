from pydantic import BaseModel
from typing import Optional


class ViolationCreate(BaseModel):
    inspection_id: int
    rule_id: int
    status: str
    detected_value: Optional[str] = None
    expected_value: Optional[str] = None
    message: Optional[str] = None


class ViolationResponse(BaseModel):
    id: int
    inspection_id: int
    rule_id: int
    status: str
    detected_value: Optional[str]
    expected_value: Optional[str]
    message: Optional[str]