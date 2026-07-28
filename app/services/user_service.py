from sqlalchemy.orm import Session
from app.models.user import User

def get_user_profile(user: User):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active
    }

def get_all_users(db: Session):
    return db.query(User).all()