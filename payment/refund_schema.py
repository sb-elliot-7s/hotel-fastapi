from typing import Optional

from pydantic import BaseModel
from .constants import ReasonRefund


class CreateRefundSchema(BaseModel):
    amount: Optional[int]
    reason: Optional[ReasonRefund]
