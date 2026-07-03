from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import date, timedelta

from app.models.journal import JournalEntry


def get_journal_summary(db: Session):
    total_entries = db.query(JournalEntry).count()

    avg_sleep = db.query(func.coalesce(func.avg(JournalEntry.sleep_hours), 0)).scalar()
    avg_energy = db.query(func.coalesce(func.avg(JournalEntry.energy_level), 0)).scalar()
    avg_mood = db.query(func.coalesce(func.avg(JournalEntry.mood_level), 0)).scalar()
    avg_productivity = db.query(func.coalesce(func.avg(JournalEntry.productivity_level), 0)).scalar()

    latest_entry = db.query(JournalEntry).order_by(desc(JournalEntry.log_date)).first()

    last_7_days = []
    today = date.today()
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        entry = db.query(JournalEntry).filter(JournalEntry.log_date == day).first()
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
        "latest_entry": {
            "id": latest_entry.id,
            "log_date": latest_entry.log_date,
            "energy_level": latest_entry.energy_level,
            "mood_level": latest_entry.mood_level,
            "productivity_level": latest_entry.productivity_level,
        } if latest_entry else None,
        "last_7_days": last_7_days,
    }