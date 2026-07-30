from pydantic import BaseModel


class MemberBalance(BaseModel):
    user_id: int
    name: str
    net_cents: int
