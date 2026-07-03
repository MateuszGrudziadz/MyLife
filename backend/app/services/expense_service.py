from fastapi import HTTPException
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.expense import Expense

ALLOWED_TYPES = {"wplata", "wydatek"}


def normalize_type(value: str) -> str:
    if value not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Typ musi mieć wartość: wplata albo wydatek",
        )
    return value


def get_balance(db: Session, user_id: int) -> float:
    incomes = db.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
        Expense.user_id == user_id,
        Expense.transaction_type == "wplata",
    ).scalar()

    expenses = db.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
        Expense.user_id == user_id,
        Expense.transaction_type == "wydatek",
    ).scalar()

    return float(incomes) - float(expenses)


def get_month_stats(db: Session, year: int, month: int, user_id: int):
    base_query = db.query(Expense).filter(
        Expense.user_id == user_id,
        func.extract("year", Expense.created_at) == year,
        func.extract("month", Expense.created_at) == month,
    )

    income_total = db.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
        Expense.user_id == user_id,
        Expense.transaction_type == "wplata",
        func.extract("year", Expense.created_at) == year,
        func.extract("month", Expense.created_at) == month,
    ).scalar()

    expense_total = db.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
        Expense.user_id == user_id,
        Expense.transaction_type == "wydatek",
        func.extract("year", Expense.created_at) == year,
        func.extract("month", Expense.created_at) == month,
    ).scalar()

    biggest_expense = db.query(Expense).filter(
        Expense.user_id == user_id,
        Expense.transaction_type == "wydatek",
        func.extract("year", Expense.created_at) == year,
        func.extract("month", Expense.created_at) == month,
    ).order_by(desc(Expense.amount)).first()

    top_category = db.query(
        Category.name,
        func.coalesce(func.sum(Expense.amount), 0).label("total"),
    ).join(Expense, Expense.category_id == Category.id).filter(
        Expense.user_id == user_id,
        Expense.transaction_type == "wydatek",
        func.extract("year", Expense.created_at) == year,
        func.extract("month", Expense.created_at) == month,
    ).group_by(Category.name).order_by(desc("total")).first()

    return {
        "income_total": float(income_total),
        "expense_total": float(expense_total),
        "balance": float(income_total) - float(expense_total),
        "transactions_count": base_query.count(),
        "biggest_expense": {
            "id": biggest_expense.id,
            "amount": float(biggest_expense.amount),
            "description": biggest_expense.description,
        } if biggest_expense else None,
        "top_category": {
            "name": top_category[0],
            "total": float(top_category[1]),
        } if top_category else None,
    }


def validate_category_kind(category: Category, transaction_type: str):
    if category.kind != transaction_type:
        raise HTTPException(
            status_code=400,
            detail=f"Kategoria '{category.name}' ma typ '{category.kind}', a transakcja ma typ '{transaction_type}'.",
        )