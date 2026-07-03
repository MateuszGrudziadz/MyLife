from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.journal import JournalEntry
from app.models.tag import Tag
from app.models.user import User
from app.schemas.journal import JournalEntryCreate, JournalEntryOut, JournalEntryUpdate
from app.schemas.tag import TagCreate, TagOut
from app.services.journal_service import get_journal_summary, get_or_create_tags, normalize_tag_names

router = APIRouter(prefix="/journal", tags=["journal"])


def serialize_journal_entry(entry: JournalEntry) -> dict:
    return {
        "id": entry.id,
        "log_date": entry.log_date,
        "sleep_hours": entry.sleep_hours,
        "energy_level": entry.energy_level,
        "mood_level": entry.mood_level,
        "productivity_level": entry.productivity_level,
        "calories_eaten": entry.calories_eaten,
        "caffeine_mg": entry.caffeine_mg,
        "journal_text": entry.journal_text,
        "gratitude_text": entry.gratitude_text,
        "notes": entry.notes,
        "tags": [tag.name for tag in entry.tags] if entry.tags else [],
        "created_at": entry.created_at,
        "updated_at": entry.updated_at,
    }


@router.get("/tags", response_model=list[TagOut])
def list_tags(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Tag).filter(Tag.user_id == current_user.id).order_by(Tag.name).all()


@router.post("/tags", response_model=TagOut, status_code=status.HTTP_201_CREATED)
def create_tag(
    payload: TagCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    name = normalize_tag_names([payload.name])
    if not name:
        raise HTTPException(status_code=400, detail="Nazwa taga nie może być pusta")

    existing = db.query(Tag).filter(Tag.user_id == current_user.id, Tag.name == name[0]).first()
    if existing:
        raise HTTPException(status_code=400, detail="Taki tag już istnieje")

    tag = Tag(user_id=current_user.id, name=name[0])
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


@router.delete("/tags/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tag = db.query(Tag).filter(Tag.id == tag_id, Tag.user_id == current_user.id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Nie znaleziono taga")

    db.delete(tag)
    db.commit()
    return None


@router.post("", response_model=JournalEntryOut, status_code=status.HTTP_201_CREATED)
def create_journal_entry(
    payload: JournalEntryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = db.query(JournalEntry).filter(
        JournalEntry.user_id == current_user.id,
        JournalEntry.log_date == payload.log_date,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Wpis dla tej daty już istnieje")

    entry = JournalEntry(
        user_id=current_user.id,
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
    db.flush()

    if payload.tags is not None:
        entry.tags = get_or_create_tags(db, current_user.id, payload.tags)

    db.commit()
    db.refresh(entry)
    return serialize_journal_entry(entry)


@router.get("", response_model=list[JournalEntryOut])
def list_journal_entries(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entries = db.query(JournalEntry).filter(
        JournalEntry.user_id == current_user.id,
    ).order_by(desc(JournalEntry.log_date), desc(JournalEntry.id)).all()

    return [serialize_journal_entry(entry) for entry in entries]


@router.get("/{entry_id}", response_model=JournalEntryOut)
def get_journal_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = db.query(JournalEntry).filter(
        JournalEntry.id == entry_id,
        JournalEntry.user_id == current_user.id,
    ).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Nie znaleziono wpisu")
    return serialize_journal_entry(entry)


@router.put("/{entry_id}", response_model=JournalEntryOut)
def update_journal_entry(
    entry_id: int,
    payload: JournalEntryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = db.query(JournalEntry).filter(
        JournalEntry.id == entry_id,
        JournalEntry.user_id == current_user.id,
    ).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Nie znaleziono wpisu")

    if payload.log_date is not None:
        duplicate = db.query(JournalEntry).filter(
            JournalEntry.user_id == current_user.id,
            JournalEntry.log_date == payload.log_date,
            JournalEntry.id != entry_id,
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

    if payload.tags is not None:
        entry.tags = get_or_create_tags(db, current_user.id, payload.tags)

    db.commit()
    db.refresh(entry)
    return serialize_journal_entry(entry)


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_journal_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = db.query(JournalEntry).filter(
        JournalEntry.id == entry_id,
        JournalEntry.user_id == current_user.id,
    ).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Nie znaleziono wpisu")

    db.delete(entry)
    db.commit()
    return None


@router.get("/stats/summary")
def journal_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_journal_summary(db, current_user.id)