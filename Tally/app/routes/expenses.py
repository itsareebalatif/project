from datetime import date

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app import database
from app import models
from app import schemas
from app.core import security  # Adjust import based on your actual path structure
from app.routes.groups import verify_group_membership
from app.services.expense_service import (
    create_expense_atomic,
    delete_expense_record,
    get_filtered_expenses,
)

router = APIRouter(prefix="/groups/{group_id}/expenses", tags=["Expenses"])


@router.post("", response_model=schemas.ExpenseOut, status_code=status.HTTP_201_CREATED)
def create_expense(
    group_id: int,
    data: schemas.ExpenseCreate,
    current_user: models.User = Depends(security.get_current_user),
    group=Depends(verify_group_membership),
    db: Session = Depends(database.get_db),
):
    return create_expense_atomic(group_id, data, current_user.id, db)


@router.get("", response_model=list[schemas.ExpenseOut])
def list_expenses(
    group_id: int,
    category: str | None = None,
    member_id: int | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    group=Depends(verify_group_membership),
    db: Session = Depends(database.get_db),
):
    return get_filtered_expenses(group_id, category, member_id, start_date, end_date, db)


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    group_id: int,
    expense_id: int,
    current_user: models.User = Depends(security.get_current_user),
    group=Depends(verify_group_membership),
    db: Session = Depends(database.get_db),
):
    return delete_expense_record(group_id, expense_id, current_user.id, group.created_by, db)