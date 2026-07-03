from sqlalchemy import Column, Integer, String, Date, Numeric, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class JournalEntry(Base):
    __tablename__ = "journal_entries"
    __table_args__ = (
        UniqueConstraint("user_id", "log_date", name="uq_journal_user_log_date"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    log_date = Column(Date, nullable=False, index=True)

    sleep_hours = Column(Numeric(4, 1), nullable=True)
    energy_level = Column(Integer, nullable=True)
    mood_level = Column(Integer, nullable=True)
    productivity_level = Column(Integer, nullable=True)
    calories_eaten = Column(Integer, nullable=True)
    caffeine_mg = Column(Integer, nullable=True)

    journal_text = Column(Text, nullable=True)
    gratitude_text = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="journal_entries")
    tags = relationship(
        "Tag",
        secondary="journal_entry_tags",
        back_populates="journal_entries",
        lazy="selectin",
    )