from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate

def get_all_posts(db: Session):
    return db.query(Post).all()

def get_post_by_id(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def create_post(db: Session, post_data: PostCreate, user_id: int):
    new_post = Post(
        title=post_data.title,
        content=post_data.content,
        owner_id=user_id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def update_post(db: Session, post_id: int, post_data: PostUpdate, user_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return None
    if post.owner_id != user_id:
        return "FORBIDDEN"   #restriction .....here
    
    if post_data.title is not None:
        post.title = post_data.title
    if post_data.content is not None:
        post.content = post_data.content
        
    db.commit()
    db.refresh(post)
    return post

def delete_post(db: Session, post_id: int, user_id: int, is_admin: bool = False):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return None
    if post.owner_id != user_id and not is_admin:
        return "FORBIDDEN"
        
    db.delete(post)
    db.commit()
    return True