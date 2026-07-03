from datetime import date, timedelta
from typing import Iterable

from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.models.journal import JournalEntry
from app.models.tag import Tag
from app.models.link_tables import journal_entry_tags


def normalize_tag_names(tag_names: Iterable[str] | None) -> list[str]:
    if not tag_names:
        return []

    result: list[str] = []
    seen: set[str] = set()

    for raw in tag_names:
        normalized = raw.strip().lower()
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(normalized)

    return result


def get_or_create_tags(db: Session, user_id: int, tag_names: Iterable[str] | None) -> list[Tag]:
    names = normalize_tag_names(tag_names)
    tags: list[Tag] = []

    for name in names:
        tag = db.query(Tag).filter(Tag.user_id == user_id, Tag.name == name).first()
        if not tag:
            tag = Tag(user_id=user_id, name=name)
            db.add(tag)
            db.flush()
        tags.append(tag)

    return tags


def get_journal_summary(db: Session, user_id: int):
    user_query = db.query(JournalEntry).filter(JournalEntry.user_id == user_id)

    total_entries = user_query.count()

    avg_sleep = user_query.with_entities(func.coalesce(func.avg(JournalEntry.sleep_hours), 0)).scalar()
    avg_energy = user_query.with_entities(func.coalesce(func.avg(JournalEntry.energy_level), 0)).scalar()
    avg_mood = user_query.with_entities(func.coalesce(func.avg(JournalEntry.mood_level), 0)).scalar()
    avg_productivity = user_query.with_entities(func.coalesce(func.avg(JournalEntry.productivity_level), 0)).scalar()

    latest_entry = user_query.order_by(desc(JournalEntry.log_date)).first()

    tag_count = db.query(Tag).filter(Tag.user_id == user_id).count()

    top_tags = (
        db.query(
            Tag.name,
            func.count(journal_entry_tags.c.journal_entry_id).label("usage_count"),
        )
        .join(journal_entry_tags, Tag.id == journal_entry_tags.c.tag_id)
        .filter(Tag.user_id == user_id)
        .group_by(Tag.name)
        .order_by(desc("usage_count"))
        .limit(5)
        .all()
    )

    last_7_days = []
    today = date.today()
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        entry = db.query(JournalEntry).filter(
            JournalEntry.user_id == user_id,
            JournalEntry.log_date == day,
        ).first()

        last_7_days.append({
            "date": day.isoformat(),
            "sleep_hours": float(entry.sleep_hours) if entry and entry.sleep_hours is not None else None,
            "energy_level": entry.energy_level if entry else None,
            "mood_level": entry.mood_level if entry else None,
            "productivity_level": entry.productivity_level if entry else None,
        })

    return {
        "total_entries": total_entries,
        "avg_sleep": float(avg_sleep or 0),
        "avg_energy": float(avg_energy or 0),
        "avg_mood": float(avg_mood or 0),
        "avg_productivity": float(avg_productivity or 0),
        "tag_count": tag_count,
        "top_tags": [
            {"name": name, "usage_count": int(usage_count)}
            for name, usage_count in top_tags
        ],
        "latest_entry": {
            "id": latest_entry.id,
            "log_date": latest_entry.log_date,
            "energy_level": latest_entry.energy_level,
            "mood_level": latest_entry.mood_level,
            "productivity_level": latest_entry.productivity_level,
            "tags": [tag.name for tag in latest_entry.tags] if latest_entry else [],
        } if latest_entry else None,
        "last_7_days": last_7_days,
    }