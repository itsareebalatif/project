from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token
from app.core.security import hash_password, verify_password, create_access_token
import logging

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

    # encription
    hashed_pwd = hash_password(user_data.password)

    # new user  signup
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_pwd,
        role=user_data.role
    )

    # commit
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"User signed up successfully: {new_user.email}")

    return new_user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.email == form_data.username).first()

    # check user is in the db
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials") 

    # creating token
    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    logger.info(f"User logged in successfully: {user.email}")
    return {"access_token": access_token, "token_type": "bearer"}


from app.core.dependencies import get_current_user, require_role

# Test route for everone
@router.get("/test-user-route")
def test_user_route(current_user: User = Depends(get_current_user)):
    return {
        "message": f"Hello {current_user.name}! You are logged in successfully.",
        "your_role": current_user.role
    }

# test rout for just admin
@router.get("/test-admin-route")
def test_admin_route(admin_user: User = Depends(require_role("ADMIN"))):
    return {
        "message": f"Welcome Admin {admin_user.name}! You have full clearance."
    }