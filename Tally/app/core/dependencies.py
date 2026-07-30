from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import database
from app import models
from app.core import security


# Current Authent user
def get_current_user_dependency(
    token: str = Depends(security.oauth2_scheme), db: Session = Depends(database.get_db)
):
    return security.get_current_user(token, db)


# verification of group-membership
def verify_group_membership(
    group_id: int,
    current_user: models.User = Depends(get_current_user_dependency),
    db: Session = Depends(database.get_db),
):
    # Checking if group exist or not 
    group = db.query(models.ExpenseGroup).filter(models.ExpenseGroup.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    # Check if user have membership or not
    membership = (
        db.query(models.GroupMember)
        .filter(
            models.GroupMember.group_id == group_id,
            models.GroupMember.user_id == current_user.id,
        )
        .first()
    )
    
    # NO membership found
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this group",
        )

    return group