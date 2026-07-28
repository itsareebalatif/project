from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.core.dependencies import get_current_user, require_role
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    return user_service.get_user_profile(current_user)

# Optional admin-only route using your service
@router.get("/", dependencies=[Depends(require_role("ADMIN"))])
def list_all_users(db: Session = Depends(get_db)):
    return user_service.get_all_users(db)