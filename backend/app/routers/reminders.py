from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.reminder import Reminder
from app.schemas.reminder import ReminderCreate, ReminderOut, ReminderUpdate
from app.services.reminder_service import get_all_reminders, get_active_reminders_count, get_next_reminder

router = APIRouter(prefix="/reminders", tags=["reminders"])


@router.post("", response_model=ReminderOut, status_code=status.HTTP_201_CREATED)
def create_reminder(payload: ReminderCreate, db: Session = Depends(get_db)):
    reminder = Reminder(
        title=payload.title,
        description=payload.description,
        reminder_at=payload.reminder_at,
        is_done=False,
    )
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder


@router.get("", response_model=list[ReminderOut])
def list_reminders(db: Session = Depends(get_db)):
    return get_all_reminders(db)


@router.get("/{reminder_id}", response_model=ReminderOut)
def get_reminder(reminder_id: int, db: Session = Depends(get_db)):
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Nie znaleziono przypomnienia")
    return reminder


@router.put("/{reminder_id}", response_model=ReminderOut)
def update_reminder(reminder_id: int, payload: ReminderUpdate, db: Session = Depends(get_db)):
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Nie znaleziono przypomnienia")

    if payload.title is not None:
        reminder.title = payload.title
    if payload.description is not None:
        reminder.description = payload.description
    if payload.reminder_at is not None:
        reminder.reminder_at = payload.reminder_at
    if payload.is_done is not None:
        reminder.is_done = payload.is_done

    db.commit()
    db.refresh(reminder)
    return reminder


@router.patch("/{reminder_id}/done", response_model=ReminderOut)
def mark_reminder_done(reminder_id: int, db: Session = Depends(get_db)):
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Nie znaleziono przypomnienia")

    reminder.is_done = True
    db.commit()
    db.refresh(reminder)
    return reminder


@router.delete("/{reminder_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reminder(reminder_id: int, db: Session = Depends(get_db)):
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Nie znaleziono przypomnienia")

    db.delete(reminder)
    db.commit()
    return None


@router.get("/stats/summary")
def reminders_summary(db: Session = Depends(get_db)):
    next_reminder = get_next_reminder(db)
    return {
        "active_count": get_active_reminders_count(db),
        "next_reminder": {
            "id": next_reminder.id,
            "title": next_reminder.title,
            "reminder_at": next_reminder.reminder_at,
        } if next_reminder else None,
    }