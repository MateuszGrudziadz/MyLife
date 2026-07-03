from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CategoryCreate(BaseModel):
    name: str
    kind: str  # wplata / wydatek


class CategoryOut(BaseModel):
    id: int
    name: str
    kind: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)