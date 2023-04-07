from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.models.user import User


class CRUDDonation(CRUDBase):
    async def get_by_user(
        self, user: User, session: AsyncSession
    ) -> List[Donation]:
        donations = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
