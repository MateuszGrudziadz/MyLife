from sqlalchemy import Table, Column, Integer, ForeignKey
from app.core.database import Base

journal_entry_tags = Table(
    "journal_entry_tags",
    Base.metadata,
    Column(
        "journal_entry_id",
        Integer,
        ForeignKey("journal_entries.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        Integer,
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)