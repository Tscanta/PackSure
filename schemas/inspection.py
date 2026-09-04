from pydantic import BaseModel, Field
from typing import Optional


class InspectionCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    overall_status: str
    confidence: Optional[float] = Field(None, ge=0, le=100)


class InspectionResponse(BaseModel):
    id: int
    product_id: int
    inspection_date: Optional[str]
    overall_status: Optional[str]
    confidence: Optional[float]