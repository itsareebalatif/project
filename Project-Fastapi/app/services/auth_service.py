from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password, create_access_token
from fastapi import HTTPException,status
from sqlalchemy.exc import IntegrityError
def register_user(db: Session, user_data: UserCreate):
    try:
        
        hashed_password = get_password_hash(user_data.password)

        role = user_data.role.upper()  
    
        if role not in ["ADMIN", "USER"]:
            raise ValueError(f"Invalid role: {role}")
        
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hashed_password,
            role=user_data.role
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
        
    except IntegrityError:
        db.rollback()  
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database error: Email already exists or invalid data."
        )
    except Exception as e:
        db.rollback()  
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )



def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return access_token