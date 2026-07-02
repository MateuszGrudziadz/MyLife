from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime

from app.models.expense import Expense
from app.models.category import Category


def get_dashboard_summary(db: Session):
    income_total = db.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
        Expense.transaction_type == "income"
    ).scalar()

    expense_total = db.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
        Expense.transaction_type == "expense"
    ).scalar()

    balance = float(income_total) - float(expense_total)

    biggest_expense = db.query(Expense).filter(
        Expense.transaction_type == "expense"
    ).order_by(desc(Expense.amount)).first()

    top_category = db.query(
        Category.name,
        func.coalesce(func.sum(Expense.amount), 0).label("total")
    ).join(Expense, Expense.category_id == Category.id).filter(
        Expense.transaction_type == "expense"
    ).group_by(Category.name).order_by(desc("total")).first()

    recent_transactions = db.query(Expense).order_by(
        desc(Expense.created_at),
        desc(Expense.id)
    ).limit(5).all()

    monthly_income = db.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
        Expense.transaction_type == "income",
        func.extract("year", Expense.created_at) == datetime.now().year,
        func.extract("month", Expense.created_at) == datetime.now().month
    ).scalar()

    monthly_expense = db.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
        Expense.transaction_type == "expense",
        func.extract("year", Expense.created_at) == datetime.now().year,
        func.extract("month", Expense.created_at) == datetime.now().month
    ).scalar()

    return {
        "balance": float(balance),
        "income_total": float(income_total),
        "expense_total": float(expense_total),
        "monthly_income": float(monthly_income),
        "monthly_expense": float(monthly_expense),
        "biggest_expense": {
            "id": biggest_expense.id,
            "amount": float(biggest_expense.amount),
            "description": biggest_expense.description,
            "created_at": biggest_expense.created_at,
        } if biggest_expense else None,
        "top_category": {
            "name": top_category[0],
            "total": float(top_category[1]),
        } if top_category else None,
        "recent_transactions": [
            {
                "id": t.id,
                "transaction_type": t.transaction_type,
                "amount": float(t.amount),
                "description": t.description,
                "created_at": t.created_at,
                "category_id": t.category_id,
            }
            for t in recent_transactions
        ],
    }