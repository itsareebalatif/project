from sqlalchemy import Column, Integer, String, Boolean,Enum
from sqlalchemy.orm import relationship
from app.database import Base
from app.core.role import Role

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.USER) # e.g., "user" or "admin"
    is_active = Column(Boolean, default=True)

    # Relationships
    posts = relationship("Post", back_populates="owner", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")