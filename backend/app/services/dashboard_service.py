from datetime import datetime, timedelta, date
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.expense import Expense
from app.models.reminder import Reminder
from app.services.journal_service import get_journal_summary
from app.services.reminder_service import get_reminders_summary


def get_dashboard_summary(db: Session, user_id: int):
    income_total = db.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
        Expense.user_id == user_id,
        Expense.transaction_type == "wplata",
    ).scalar()

    expense_total = db.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
        Expense.user_id == user_id,
        Expense.transaction_type == "wydatek",
    ).scalar()

    balance = float(income_total) - float(expense_total)

    biggest_expense = db.query(Expense).filter(
        Expense.user_id == user_id,
        Expense.transaction_type == "wydatek",
    ).order_by(desc(Expense.amount)).first()

    top_category = db.query(
        Category.name,
        func.coalesce(func.sum(Expense.amount), 0).label("total"),
    ).join(Expense, Expense.category_id == Category.id).filter(
        Expense.user_id == user_id,
        Expense.transaction_type == "wydatek",
    ).group_by(Category.name).order_by(desc("total")).first()

    recent_transactions = db.query(Expense).filter(
        Expense.user_id == user_id,
    ).order_by(desc(Expense.created_at), desc(Expense.id)).limit(5).all()

    now = datetime.now()

    monthly_income = db.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
        Expense.user_id == user_id,
        Expense.transaction_type == "wplata",
        func.extract("year", Expense.created_at) == now.year,
        func.extract("month", Expense.created_at) == now.month,
    ).scalar()

    monthly_expense = db.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
        Expense.user_id == user_id,
        Expense.transaction_type == "wydatek",
        func.extract("year", Expense.created_at) == now.year,
        func.extract("month", Expense.created_at) == now.month,
    ).scalar()

    category_breakdown = db.query(
        Category.name,
        func.coalesce(func.sum(Expense.amount), 0).label("total"),
    ).join(Expense, Expense.category_id == Category.id).filter(
        Expense.user_id == user_id,
        Expense.transaction_type == "wydatek",
    ).group_by(Category.name).order_by(desc("total")).all()

    last_6_months = []
    for i in range(5, -1, -1):
        month_date = now - timedelta(days=30 * i)
        year = month_date.year
        month = month_date.month

        month_total = db.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
            Expense.user_id == user_id,
            Expense.transaction_type == "wydatek",
            func.extract("year", Expense.created_at) == year,
            func.extract("month", Expense.created_at) == month,
        ).scalar()

        last_6_months.append({
            "month": f"{year}-{month:02d}",
            "total": float(month_total),
        })

    journal_summary = get_journal_summary(db, user_id)
    reminder_summary = get_reminders_summary(db, user_id)

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
        "category_breakdown": [
            {"name": name, "total": float(total)}
            for name, total in category_breakdown
        ],
        "last_6_months": last_6_months,
        "active_reminders_count": reminder_summary["active_count"],
        "next_reminder": reminder_summary["next_reminder"],
        "latest_journal": journal_summary["latest_entry"],
        "avg_sleep": journal_summary["avg_sleep"],
        "avg_energy": journal_summary["avg_energy"],
        "avg_mood": journal_summary["avg_mood"],
        "avg_productivity": journal_summary["avg_productivity"],
        "journal_total_entries": journal_summary["total_entries"],
        "tag_count": journal_summary["tag_count"],
        "top_tags": journal_summary["top_tags"],
        "last_7_days_journal": journal_summary["last_7_days"],
    }