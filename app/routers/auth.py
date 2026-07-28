import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token
from app.core.dependencies import get_current_user, require_role
from app.services import auth_service  # 👉 Import your new service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered"
        )
    
    new_user = auth_service.register_user(db, user_data)
    logger.info(f"User signed up successfully: {new_user.email}")
    return new_user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    access_token = auth_service.authenticate_user(db, form_data.username, form_data.password)
    
    if not access_token:
        logger.warning(f"Failed login attempt for: {form_data.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials") 

    logger.info(f"User logged in successfully: {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/test-user-route")
def test_user_route(current_user: User = Depends(get_current_user)):
    return {
        "message": f"Hello {current_user.name}! You are logged in successfully.",
        "your_role": current_user.role
    }


@router.get("/test-admin-route")
def test_admin_route(admin_user: User = Depends(require_role("ADMIN"))):
    return {
        "message": f"Welcome Admin {admin_user.name}! You have full clearance."
    }