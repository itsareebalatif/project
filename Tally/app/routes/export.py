from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app import database
from app import models
from app.routes.groups import verify_group_membership
from app.services.export_service import generate_expenses_csv_string

router = APIRouter(prefix="/groups/{group_id}", tags=["Export"])


@router.get("/export.csv")
def export_expenses_csv(
    group_id: int,
    group=Depends(verify_group_membership),
    db: Session = Depends(database.get_db),
):
    # 1. Fetch all expenses for this group
    expenses = (
        db.query(models.Expense)
        .filter(models.Expense.group_id == group_id)
        .order_by(models.Expense.created_at.desc())
        .all()
    )

    # via service
    csv_data = generate_expenses_csv_string(expenses)

    # 3. Return as a downloadable streaming response
    return StreamingResponse(
        iter([csv_data]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=group_{group_id}_expenses.csv"
        },
    )