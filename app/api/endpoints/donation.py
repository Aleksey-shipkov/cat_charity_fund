from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.core.user import current_superuser, current_user
from app.models.charity_project import CharityProject
from app.models.user import User
from app.schemas.donation import (
    DonationBriefDB,
    DonationFullDB,
    DonationCreate,
)
from app.servises.investing import check_uninvested_amounts


router = APIRouter()


@router.post(
    "/", response_model=DonationBriefDB, response_model_exclude_none=True
)
async def create_donation(
    obj_in: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(obj_in, session, user)
    new_donation = await check_uninvested_amounts(
        CharityProject, new_donation, session
    )
    return new_donation


@router.get(
    "/",
    response_model=List[DonationFullDB],
    response_model_exclude_none=True,
    dependencies=(Depends(current_superuser),),
)
async def get_all_donation(session: AsyncSession = Depends(get_async_session)):
    donations = await donation_crud.get_all(session)
    return donations


@router.get(
    "/my",
    response_model=List[DonationBriefDB],
    response_model_exclude_none=True,
)
async def get_user_donation(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    donations = await donation_crud.get_by_user(user, session)
    return donations
