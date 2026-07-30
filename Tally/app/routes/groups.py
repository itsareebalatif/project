from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import database
import models
import schemas
from core.dependencies import get_current_user_dependency, verify_group_membership
from services.group_service import (
    add_member_to_group,
    create_group_record,
    list_user_groups,
)

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.post("", response_model=schemas.GroupOut, status_code=201)
def create_group(
    group_data: schemas.GroupCreate,
    current_user: models.User = Depends(get_current_user_dependency),
    db: Session = Depends(database.get_db),
):
    return create_group_record(group_data, current_user.id, db)


@router.get("", response_model=list[schemas.GroupOut])
def list_my_groups(
    current_user: models.User = Depends(get_current_user_dependency),
    db: Session = Depends(database.get_db),
):
    return list_user_groups(current_user.id, db)


@router.post("/{group_id}/members", status_code=201)
def add_member(
    group_id: int,
    payload: schemas.GroupMemberAdd,
    group=Depends(verify_group_membership),
    db: Session = Depends(database.get_db),
):
    return add_member_to_group(group_id, payload, db)


@router.get("/{group_id}", response_model=schemas.GroupOut)
def get_group_details(
    group: models.ExpenseGroup = Depends(verify_group_membership),
):
    return group