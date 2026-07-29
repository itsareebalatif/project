from pydantic import BaseModel
from datetime import datetime
from app.schemas.user import UserResponse

class CommentCreate(BaseModel):
    body: str

class CommentUpdate(BaseModel):
    body: str

class CommentResponse(BaseModel):
    id: int
    body: str
    post_id: int
    author_id: int
    created_at: datetime
    author: UserResponse  

    class Config:
        from_attributes = True