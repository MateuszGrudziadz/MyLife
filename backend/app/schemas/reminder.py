from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class ReminderCreate(BaseModel):
    title: str
    description: Optional[str] = None
    reminder_at: datetime


class ReminderUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    reminder_at: Optional[datetime] = None
    is_done: Optional[bool] = None


class ReminderOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    reminder_at: datetime
    is_done: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)