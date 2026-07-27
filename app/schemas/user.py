from pydantic import BaseModel, EmailStr

#Input.py for the user
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "user"  

#output.py for the user
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        from_attributes = True

        