from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, model_validator


class ExpenseSplitCreate(BaseModel):
    user_id: int
    share_cents: int


class ExpenseCreate(BaseModel):
    description: str
    amount_cents: int
    category: str | None = None
    splits: list[ExpenseSplitCreate]

    @model_validator(mode="after")
    def splits_must_sum_to_amount(self) -> "ExpenseCreate":
        if sum(split.share_cents for split in self.splits) != self.amount_cents:
            raise ValueError("split amounts must sum to the expense amount")
        return self


class ExpenseSplitOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    share_cents: int


class ExpenseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    group_id: int
    description: str
    amount_cents: int
    category: str | None
    paid_by: int
    created_at: datetime
    splits: list[ExpenseSplitOut]


class ExpenseFilter(BaseModel):
    category: str | None = None
    member_id: int | None = None
    start_date: date | None = None
    end_date: date | None = None
