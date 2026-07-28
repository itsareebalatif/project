from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate

def get_comments_for_post(db: Session, post_id: int):
    return db.query(Comment).filter(Comment.post_id == post_id).all()

def create_comment(db: Session, comment_data: CommentCreate, post_id: int, user_id: int):
    new_comment = Comment(
        body=comment_data.body,
        post_id=post_id,
        author_id=user_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def update_comment(db: Session, comment_id: int, comment_data: CommentUpdate, user_id: int):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        return None
    if comment.author_id != user_id:
        return "FORBIDDEN"
        
    comment.body = comment_data.body
    db.commit()
    db.refresh(comment)
    return comment

def delete_comment(db: Session, comment_id: int, user_id: int, is_admin: bool = False):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        return None
    if comment.author_id != user_id and not is_admin:
        return "FORBIDDEN"
        
    db.delete(comment)
    db.commit()
    return True