from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.category import Category
from app.models.expense import Expense
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryOut
from app.schemas.expense import ExpenseCreate, ExpenseOut, ExpenseUpdate
from app.services.expense_service import (
    ALLOWED_TYPES,
    get_balance,
    get_month_stats,
    normalize_type,
    validate_category_kind,
)

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("/categories", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = db.query(Category).filter(
        Category.user_id == current_user.id,
        Category.name == payload.name,
        Category.kind == normalize_type(payload.kind),
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Taka kategoria już istnieje")

    category = Category(
        user_id=current_user.id,
        name=payload.name,
        kind=normalize_type(payload.kind),
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.get("/categories", response_model=list[CategoryOut])
def list_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Category).filter(Category.user_id == current_user.id).order_by(Category.id).all()


@router.post("/transactions", response_model=ExpenseOut, status_code=status.HTTP_201_CREATED)
def create_transaction(
    payload: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction_type = normalize_type(payload.transaction_type)

    if payload.category_id is not None:
        category = db.query(Category).filter(
            Category.id == payload.category_id,
            Category.user_id == current_user.id,
        ).first()
        if not category:
            raise HTTPException(status_code=404, detail="Nie znaleziono kategorii")
        validate_category_kind(category, transaction_type)

    transaction = Expense(
        user_id=current_user.id,
        transaction_type=transaction_type,
        amount=payload.amount,
        description=payload.description,
        category_id=payload.category_id,
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


@router.get("/transactions", response_model=list[ExpenseOut])
def list_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Expense).filter(Expense.user_id == current_user.id).order_by(desc(Expense.created_at), desc(Expense.id)).all()


@router.get("/transactions/{transaction_id}", response_model=ExpenseOut)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction = db.query(Expense).filter(
        Expense.id == transaction_id,
        Expense.user_id == current_user.id,
    ).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Nie znaleziono transakcji")
    return transaction


@router.put("/transactions/{transaction_id}", response_model=ExpenseOut)
def update_transaction(
    transaction_id: int,
    payload: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction = db.query(Expense).filter(
        Expense.id == transaction_id,
        Expense.user_id == current_user.id,
    ).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Nie znaleziono transakcji")

    if payload.transaction_type is not None:
        transaction.transaction_type = normalize_type(payload.transaction_type)

    if payload.amount is not None:
        transaction.amount = payload.amount

    if payload.description is not None:
        transaction.description = payload.description

    if payload.category_id is not None:
        category = db.query(Category).filter(
            Category.id == payload.category_id,
            Category.user_id == current_user.id,
        ).first()
        if not category:
            raise HTTPException(status_code=404, detail="Nie znaleziono kategorii")
        validate_category_kind(category, transaction.transaction_type)
        transaction.category_id = payload.category_id

    db.commit()
    db.refresh(transaction)
    return transaction


@router.delete("/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction = db.query(Expense).filter(
        Expense.id == transaction_id,
        Expense.user_id == current_user.id,
    ).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Nie znaleziono transakcji")

    db.delete(transaction)
    db.commit()
    return None


@router.get("/balance")
def balance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return {"balance": get_balance(db, current_user.id)}


@router.get("/stats/monthly")
def monthly_stats(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_month_stats(db, year, month, current_user.id)