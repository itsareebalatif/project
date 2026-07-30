from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import database
from app import models
from app import schemas
from app.core import security
from app.services.auth_service import authenticate_user_login, register_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=schemas.UserOut, status_code=201)
def register(user_data: schemas.UserCreate, db: Session = Depends(database.get_db)):
    return register_user(user_data, db)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    return authenticate_user_login(form_data, db)


@router.get("/me", response_model=schemas.UserOut)
def get_me(current_user: models.User = Depends(security.get_current_user)):
    return current_user