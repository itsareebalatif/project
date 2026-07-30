from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class GroupMember(Base):
    __tablename__ = "group_members"  

    group_id = Column(Integer, ForeignKey("expense_groups.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    # Relationships
    group = relationship("ExpenseGroup", back_populates="members")
    user = relationship("User", back_populates="group_memberships")
