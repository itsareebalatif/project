from fastapi import HTTPException
from sqlalchemy.orm import Session
import models
import schemas


def create_group_record(group_data: schemas.GroupCreate, current_user_id: int, db: Session):
    new_group = models.ExpenseGroup(name=group_data.name, created_by=current_user_id)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)

    creator_membership = models.GroupMember(group_id=new_group.id, user_id=current_user_id)
    db.add(creator_membership)
    db.commit()

    return new_group


def list_user_groups(current_user_id: int, db: Session):
    return (
        db.query(models.ExpenseGroup)
        .join(models.GroupMember)
        .filter(models.GroupMember.user_id == current_user_id)
        .all()
    )


def add_member_to_group(group_id: int, payload: schemas.GroupMemberAdd, db: Session):
    user_to_add = db.query(models.User).filter(models.User.id == payload.user_id).first()
    if not user_to_add:
        raise HTTPException(status_code=404, detail="User not found")

    existing_membership = (
        db.query(models.GroupMember)
        .filter(models.GroupMember.group_id == group_id, models.GroupMember.user_id == user_to_add.id)
        .first()
    )
    if existing_membership:
        raise HTTPException(status_code=400, detail="User is already in the group")

    new_membership = models.GroupMember(group_id=group_id, user_id=user_to_add.id)
    db.add(new_membership)
    db.commit()

    return {"detail": f"User {user_to_add.email} added to group successfully"}