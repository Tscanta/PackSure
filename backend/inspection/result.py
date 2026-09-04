from typing import Optional

from pydantic import BaseModel


class CheckResult(BaseModel):
    """
    Result of a single compliance validation check.
    """

    field: str
    status: str
    message: str

    rule_id: Optional[str] = None
    severity: Optional[str] = None
    mandatory: Optional[bool] = None