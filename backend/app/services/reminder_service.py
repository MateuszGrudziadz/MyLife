from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import asc

from app.models.reminder import Reminder


def get_reminders_summary(db: Session, user_id: int):
    query = db.query(Reminder).filter(Reminder.user_id == user_id)

    active_count = query.filter(Reminder.is_done == False).count()  # noqa: E712

    next_reminder = query.filter(
        Reminder.is_done == False,  # noqa: E712
        Reminder.reminder_at >= datetime.now(timezone.utc),
    ).order_by(asc(Reminder.reminder_at)).first()

    return {
        "active_count": active_count,
        "next_reminder": {
            "id": next_reminder.id,
            "title": next_reminder.title,
            "reminder_at": next_reminder.reminder_at,
        } if next_reminder else None,
    }