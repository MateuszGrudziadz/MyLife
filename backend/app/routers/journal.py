from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.core.database import get_db
from app.models.journal import JournalEntry
from app.schemas.journal import JournalEntryCreate, JournalEntryOut, JournalEntryUpdate
from app.services.journal_service import get_journal_summary

router = APIRouter(prefix="/journal", tags=["journal"])


@router.post("", response_model=JournalEntryOut, status_code=status.HTTP_201_CREATED)
def create_journal_entry(payload: JournalEntryCreate, db: Session = Depends(get_db)):
    existing = db.query(JournalEntry).filter(JournalEntry.log_date == payload.log_date).first()
    if existing:
        raise HTTPException(status_code=400, detail="Wpis dla tej daty już istnieje")

    entry = JournalEntry(
        log_date=payload.log_date,
        sleep_hours=payload.sleep_hours,
        energy_level=payload.energy_level,
        mood_level=payload.mood_level,
        productivity_level=payload.productivity_level,
        calories_eaten=payload.calories_eaten,
        caffeine_mg=payload.caffeine_mg,
        journal_text=payload.journal_text,
        gratitude_text=payload.gratitude_text,
        notes=payload.notes,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.get("", response_model=list[JournalEntryOut])
def list_journal_entries(db: Session = Depends(get_db)):
    return db.query(JournalEntry).order_by(desc(JournalEntry.log_date), desc(JournalEntry.id)).all()


@router.get("/{entry_id}", response_model=JournalEntryOut)
def get_journal_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(JournalEntry).filter(JournalEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Nie znaleziono wpisu")
    return entry


@router.put("/{entry_id}", response_model=JournalEntryOut)
def update_journal_entry(entry_id: int, payload: JournalEntryUpdate, db: Session = Depends(get_db)):
    entry = db.query(JournalEntry).filter(JournalEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Nie znaleziono wpisu")

    if payload.log_date is not None:
        duplicate = db.query(JournalEntry).filter(
            JournalEntry.log_date == payload.log_date,
            JournalEntry.id != entry_id
        ).first()
        if duplicate:
            raise HTTPException(status_code=400, detail="Wpis dla tej daty już istnieje")
        entry.log_date = payload.log_date

    if payload.sleep_hours is not None:
        entry.sleep_hours = payload.sleep_hours
    if payload.energy_level is not None:
        entry.energy_level = payload.energy_level
    if payload.mood_level is not None:
        entry.mood_level = payload.mood_level
    if payload.productivity_level is not None:
        entry.productivity_level = payload.productivity_level
    if payload.calories_eaten is not None:
        entry.calories_eaten = payload.calories_eaten
    if payload.caffeine_mg is not None:
        entry.caffeine_mg = payload.caffeine_mg
    if payload.journal_text is not None:
        entry.journal_text = payload.journal_text
    if payload.gratitude_text is not None:
        entry.gratitude_text = payload.gratitude_text
    if payload.notes is not None:
        entry.notes = payload.notes

    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_journal_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(JournalEntry).filter(JournalEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Nie znaleziono wpisu")

    db.delete(entry)
    db.commit()
    return None


@router.get("/stats/summary")
def journal_summary(db: Session = Depends(get_db)):
    return get_journal_summary(db)