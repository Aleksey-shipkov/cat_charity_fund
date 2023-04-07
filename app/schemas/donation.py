from typing import Optional
from datetime import datetime
from pydantic import BaseModel, PositiveInt


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = "forbid"


class DonationBriefDB(DonationCreate):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationFullDB(DonationBriefDB):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
