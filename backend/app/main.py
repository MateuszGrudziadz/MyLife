from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine

from app.models.user import User
from app.models.category import Category
from app.models.expense import Expense
from app.models.reminder import Reminder
from app.models.journal import JournalEntry
from app.models.tag import Tag
from app.models.link_tables import journal_entry_tags  # noqa: F401

from app.routers import auth, dashboard, expenses, reminders, journal

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MyLife")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(expenses.router)
app.include_router(reminders.router)
app.include_router(journal.router)


@app.get("/")
def root():
    return {"message": "MyLife API działa"}