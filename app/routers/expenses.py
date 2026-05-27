from fastapi import APIRouter, Request
from app.services.expense_analysis.wydatki import oblicz_stan_konta

router = APIRouter(prefix="/expenses", tags=["expenses"])

@router.get("/balance")
def get_balance():
    return {"balance": oblicz_stan_konta()}