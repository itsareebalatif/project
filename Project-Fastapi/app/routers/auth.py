import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import jwt
from pydantic import BaseModel, EmailStr 

from app.database import get_db
from app.models.user import User
from app.schemas.auth import UserLoginSchema, RefreshTokenSchema
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token
from app.core.dependencies import get_current_user, require_role
from app.core.security import (
    SECRET_KEY, 
    ALGORITHM, 
    create_access_token, 
    create_refresh_token
)
from app.services import auth_service
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
    return UserResponse.model_validate(new_user)


# @router.post("/login", response_model=Token)
# def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     access_token = auth_service.authenticate_user(db, form_data.username, form_data.password)
    
#     if not access_token:
#         logger.warning(f"Failed login attempt for: {form_data.username}")
#         raise HTTPException(status_code=401, detail="Invalid credentials") 

#     logger.info(f"User logged in successfully: {form_data.username}")
#     return {"access_token": access_token, "token_type": "bearer"}


# @router.get("/test-user-route")
# def test_user_route(current_user: User = Depends(get_current_user)):
#     return {
#         "message": f"Hello {current_user.name}! You are logged in successfully.",
#         "your_role": current_user.role
#     }
# @router.post("/login", response_model=Token)
# def login()


# @router.get("/test-admin-route")
# def test_admin_route(admin_user: User = Depends(require_role("ADMIN"))):
#     return {
#         "message": f"Welcome Admin {admin_user.name}! You have full clearance."
#     }


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


@router.post("/login", response_model=Token)

def login(login_data: UserLoginSchema, db: Session = Depends(get_db)):
    # 1. Authenticate credentials and get the access token
    access_token = auth_service.authenticate_user(db, login_data.email, login_data.password)
    
    if not access_token:
        logger.warning(f"Failed login attempt for: {login_data.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials") 

    # 2. Fetch the user to generate the refresh token
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    logger.info(f"User logged in successfully: {login_data.email}")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=Token)
def refresh_access_token(body: RefreshTokenSchema, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token",
    )
    try:
        payload = jwt.decode(body.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        
        if payload.get("type") != "refresh":
            raise credentials_exception
            
        user_id_str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
            
        user_id = int(user_id_str)
            
    except (jwt.PyJWTError, ValueError): 
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise credentials_exception

    
    # new_access_token = create_access_token(data={"sub": user.email})
    # new_refresh_token = create_refresh_token(data={"sub": user.email})

    new_access_token=create_access_token(data={"sub": str(user.id)})
    new_refresh_token=create_refresh_token(data={"sub": str(user.id)})
    
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token, 
        "token_type": "bearer"
    }