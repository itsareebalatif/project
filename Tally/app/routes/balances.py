from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import database
import schemas
from routes.groups import verify_group_membership
from services.balance_service import calculate_group_balances

router = APIRouter(prefix="/groups/{group_id}/balances", tags=["Balances"])

@router.get("", response_model=list[schemas.MemberBalance])
def get_group_balances(
    group_id: int,
    group=Depends(verify_group_membership),
    db: Session = Depends(database.get_db),
):
    return calculate_group_balances(group_id, db)