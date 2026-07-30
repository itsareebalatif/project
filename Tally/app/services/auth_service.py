from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app import models
from app import schemas
from app.core import security


def register_user(user_data: schemas.UserCreate, db: Session):
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = security.get_password_hash(user_data.password)
    new_user = models.User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_pwd
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user_login(form_data, db: Session):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    #if the mail doesnot match or password doesn't match it will throw error
    if not user or not security.verify_password(form_data.password, user.hashed_password):
       raise HTTPException(401, "Incorrect email or password")


    # if both matches we will use user.id for the token 
    access_token = security.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}