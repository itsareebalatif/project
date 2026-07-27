from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.core.security import SECRET_KEY, ALGORITHM



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub") 
    except:
        raise HTTPException(status_code=401, detail="Invalid Token or may be expired")

    user = db.query(User).filter(User.email == email).first()
    
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
        
    return user

def require_role(allowed_role: str):
    """Reusable dependency to restrict routes to a specific role (e.g., 'admin')."""
    def role_dependency(current_user: User = Depends(get_current_user)):
        if current_user.role != allowed_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action"
            )
        return current_user
    return role_dependency