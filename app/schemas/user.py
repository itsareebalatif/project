from pydantic import BaseModel, EmailStr,field_validator

#Input.py for the user
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "user"  

    @field_validator("email")
    @classmethod
    def validate_gmail_only(cls, value: str) -> str:
        email_lower = value.lower()
        
        if not email_lower.endswith("@gmail.com"):
            raise ValueError("Only @gmail.com email addresses are allowed.")
            
        return value

#output.py for the user
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool

    

    class Config:
        from_attributes = True

        