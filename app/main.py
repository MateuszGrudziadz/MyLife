from fastapi import FastAPI
from app.routers import users
from app.routers import expenses

app = FastAPI()

app.include_router(users.router)

app.include_router(expenses.router)