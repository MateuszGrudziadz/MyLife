from sqlalchemy import Column, Integer, String, Date, Numeric, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True, index=True)
    log_date = Column(Date, nullable=False, unique=True, index=True)

    sleep_hours = Column(Numeric(4, 1), nullable=True)          # np. 7.5
    energy_level = Column(Integer, nullable=True)               # 1-10
    mood_level = Column(Integer, nullable=True)                 # 1-10
    productivity_level = Column(Integer, nullable=True)         # 1-10
    calories_eaten = Column(Integer, nullable=True)
    caffeine_mg = Column(Integer, nullable=True)

    journal_text = Column(Text, nullable=True)
    gratitude_text = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())