from sqlalchemy.orm import Session
from sqlalchemy import asc
from datetime import datetime

from app.models.reminder import Reminder


def get_active_reminders_count(db: Session) -> int:
    return db.query(Reminder).filter(Reminder.is_done == False).count()  # noqa: E712


def get_next_reminder(db: Session):
    return (
        db.query(Reminder)
        .filter(Reminder.is_done == False, Reminder.reminder_at >= datetime.now())  # noqa: E712
        .order_by(asc(Reminder.reminder_at))
        .first()
    )


def get_all_reminders(db: Session):
    return db.query(Reminder).order_by(asc(Reminder.is_done), asc(Reminder.reminder_at)).all()