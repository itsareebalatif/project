from pydantic import BaseModel
from datetime import datetime
from app.schemas.user import UserResponse

class PostCreate(BaseModel):
    title: str
    content: str

class PostUpdate(BaseModel):
    title: str
    content: str

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int
    created_at: datetime
    owner: UserResponse   #giving output in json (all detail of user)

    class Config:
        from_attributes = True