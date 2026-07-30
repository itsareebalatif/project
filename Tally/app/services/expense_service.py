from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
import models
import schemas


def create_expense_atomic(group_id: int, data: schemas.ExpenseCreate, paid_by: int, db: Session):
    member_ids = {
        row.user_id
        for row in db.query(models.GroupMember.user_id).filter(models.GroupMember.group_id == group_id).all()
    }
    involved_ids = {paid_by} | {s.user_id for s in data.splits}
    if not involved_ids.issubset(member_ids):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="paid_by and all split users must be members of the group",
        )

    try:
        # Step A: Save the main expense
        expense = models.Expense(
            group_id=group_id,
            description=data.description,
            amount_cents=data.amount_cents,
            category=data.category,
            paid_by=paid_by,
        )
        db.add(expense)
        db.flush()  # Gets the new expense.id without final commit

        # Step B: Save all split rows
        for s in data.splits:
            split = models.ExpenseSplit(
                expense_id=expense.id,
                user_id=s.user_id,
                share_cents=s.share_cents,
            )
            db.add(split)

        # Step C: Save everything together permanently
        db.commit()
        db.refresh(expense)
        return expense

    except SQLAlchemyError:
        db.rollback()  # If anything fails, undo everything!
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not save expense and splits.",
        )


def get_filtered_expenses(group_id: int, category: str | None, member_id: int | None, db: Session):
    query = db.query(models.Expense).filter(models.Expense.group_id == group_id)

    if category:
        query = query.filter(models.Expense.category == category)

    if member_id:
        query = query.join(models.ExpenseSplit).filter(
            (models.Expense.paid_by == member_id) | (models.ExpenseSplit.user_id == member_id)
        ).distinct()

    return query.order_by(models.Expense.created_at.desc()).all()


def delete_expense_record(group_id: int, expense_id: int, current_user_id: int, group_creator_id: int, db: Session):
    expense = db.query(models.Expense).filter_by(id=expense_id, group_id=group_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    if expense.paid_by != current_user_id and group_creator_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this expense")

    db.delete(expense)
    db.commit()
    return None