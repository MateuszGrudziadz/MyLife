from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, datetime
from decimal import Decimal


class JournalEntryCreate(BaseModel):
    log_date: date
    sleep_hours: Optional[Decimal] = None
    energy_level: Optional[int] = None
    mood_level: Optional[int] = None
    productivity_level: Optional[int] = None
    calories_eaten: Optional[int] = None
    caffeine_mg: Optional[int] = None
    journal_text: Optional[str] = None
    gratitude_text: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[list[str]] = None


class JournalEntryUpdate(BaseModel):
    log_date: Optional[date] = None
    sleep_hours: Optional[Decimal] = None
    energy_level: Optional[int] = None
    mood_level: Optional[int] = None
    productivity_level: Optional[int] = None
    calories_eaten: Optional[int] = None
    caffeine_mg: Optional[int] = None
    journal_text: Optional[str] = None
    gratitude_text: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[list[str]] = None


class JournalEntryOut(BaseModel):
    id: int
    log_date: date
    sleep_hours: Optional[Decimal]
    energy_level: Optional[int]
    mood_level: Optional[int]
    productivity_level: Optional[int]
    calories_eaten: Optional[int]
    caffeine_mg: Optional[int]
    journal_text: Optional[str]
    gratitude_text: Optional[str]
    notes: Optional[str]
    tags: list[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)