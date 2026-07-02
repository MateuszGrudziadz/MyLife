from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from fastapi import HTTPException

from app.models.category import Category
from app.models.expense import Expense


def get_balance(db: Session) -> float:
    incomes = db.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
        Expense.transaction_type == "income"
    ).scalar()

    expenses = db.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
        Expense.transaction_type == "expense"
    ).scalar()

    return float(incomes) - float(expenses)


def get_month_stats(db: Session, year: int, month: int):
    base_query = db.query(Expense).filter(
        func.extract("year", Expense.created_at) == year,
        func.extract("month", Expense.created_at) == month
    )

    income_total = db.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
        Expense.transaction_type == "income",
        func.extract("year", Expense.created_at) == year,
        func.extract("month", Expense.created_at) == month
    ).scalar()

    expense_total = db.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
        Expense.transaction_type == "expense",
        func.extract("year", Expense.created_at) == year,
        func.extract("month", Expense.created_at) == month
    ).scalar()

    biggest_expense = db.query(Expense).filter(
        Expense.transaction_type == "expense",
        func.extract("year", Expense.created_at) == year,
        func.extract("month", Expense.created_at) == month
    ).order_by(desc(Expense.amount)).first()

    top_category = db.query(
        Category.name,
        func.coalesce(func.sum(Expense.amount), 0).label("total")
    ).join(Expense, Expense.category_id == Category.id).filter(
        Expense.transaction_type == "expense",
        func.extract("year", Expense.created_at) == year,
        func.extract("month", Expense.created_at) == month
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
            detail=f"Kategoria '{category.name}' ma typ '{category.kind}', a transakcja ma typ '{transaction_type}'."
        )