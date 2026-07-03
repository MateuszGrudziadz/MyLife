from pydantic import BaseModel, ConfigDict
from typing import Optional
from decimal import Decimal
from datetime import datetime


class ExpenseCreate(BaseModel):
    transaction_type: str  # wplata / wydatek / income / expense
    amount: Decimal
    description: Optional[str] = None
    category_id: Optional[int] = None


class ExpenseUpdate(BaseModel):
    transaction_type: Optional[str] = None
    amount: Optional[Decimal] = None
    description: Optional[str] = None
    category_id: Optional[int] = None


class ExpenseOut(BaseModel):
    id: int
    transaction_type: str
    amount: Decimal
    description: Optional[str]
    category_id: Optional[int]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)