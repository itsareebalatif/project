from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from app.core.dependencies import get_current_user
from app.services import comment_service

router = APIRouter(prefix="/posts/{post_id}/comments", tags=["Comments"])

@router.get("/", response_model=List[CommentResponse])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    return comment_service.get_comments_for_post(db, post_id)

@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def add_comment(post_id: int, comment_data: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return comment_service.create_comment(db, comment_data, post_id, current_user.id)

@router.put("/{comment_id}", response_model=CommentResponse)
def update_comment(post_id: int, comment_id: int, comment_data: CommentUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    is_admin = current_user.role.value == "ADMIN" if hasattr(current_user.role, "value") else current_user.role == "ADMIN"
    updated = comment_service.update_comment(db, comment_id, comment_data, current_user.id)
    if updated is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if updated == "FORBIDDEN":
        raise HTTPException(status_code=403, detail="Not authorized to edit this comment")
    return updated

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(post_id: int, comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    is_admin = current_user.role.value == "ADMIN" if hasattr(current_user.role, "value") else current_user.role == "ADMIN"
    result = comment_service.delete_comment(db, comment_id, current_user.id, is_admin)
    if result is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if result == "FORBIDDEN":
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    return None