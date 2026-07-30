from sqlalchemy import func
from sqlalchemy.orm import Session
import models
import schemas


def calculate_group_balances(group_id: int, db: Session):
    # 1. Get all members belonging to this group
    members = (
        db.query(models.User)
        .join(models.GroupMember)
        .filter(models.GroupMember.group_id == group_id)
        .all()
    )

    balances = []

    for member in members:
        # 2. Calculate total cents paid
        total_paid = (
            db.query(func.coalesce(func.sum(models.Expense.amount_cents), 0))
            .filter(
                models.Expense.group_id == group_id,
                models.Expense.paid_by == member.id,
            )
            .scalar()
        )

        # 3. Calculate total cents owed
        total_owed = (
            db.query(func.coalesce(func.sum(models.ExpenseSplit.share_cents), 0))
            .join(models.Expense, models.ExpenseSplit.expense_id == models.Expense.id)
            .filter(
                models.Expense.group_id == group_id,
                models.ExpenseSplit.user_id == member.id,
            )
            .scalar()
        )

        net_cents = total_paid - total_owed

        balances.append(
            schemas.MemberBalance(
                user_id=member.id,
                name=member.name,
                net_cents=net_cents,
            )
        )

    return balances