from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.core.dependencies import get_current_user
from app.services import post_service

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    return post_service.get_all_posts(db)

@router.get("/{post_id}", response_model=PostResponse)
def get_single_post(post_id: int, db: Session = Depends(get_db)):
    post = post_service.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_new_post(post_data: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return post_service.create_post(db, post_data, current_user.id)

@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post_data: PostUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    is_admin = current_user.role.value == "ADMIN" if hasattr(current_user.role, "value") else current_user.role == "ADMIN"
    updated = post_service.update_post(db, post_id, post_data, current_user.id)
    if updated is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if updated == "FORBIDDEN":
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
    return updated

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    is_admin = current_user.role.value == "ADMIN" if hasattr(current_user.role, "value") else current_user.role == "ADMIN"
    result = post_service.delete_post(db, post_id, current_user.id, is_admin)
    if result is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if result == "FORBIDDEN":
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    return None