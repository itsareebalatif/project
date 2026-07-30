from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import database
from app import schemas
from app.routes.groups import verify_group_membership
from app.services.balance_service import calculate_group_balances

router = APIRouter(prefix="/groups/{group_id}/balances", tags=["Balances"])

@router.get("", response_model=list[schemas.MemberBalance])
def get_group_balances(
    group_id: int,
    group=Depends(verify_group_membership),
    db: Session = Depends(database.get_db),
):
    return calculate_group_balances(group_id, db)