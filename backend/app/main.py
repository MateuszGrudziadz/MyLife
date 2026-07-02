from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine

from app.models.category import Category
from app.models.expense import Expense

from app.routers import expenses, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MyLife")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(expenses.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    return {"message": "MyLife API działa"}