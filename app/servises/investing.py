from typing import Union
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def check_uninvested_amounts(
    uninvested_obj_model: Union[CharityProject, Donation],
    new_obj: Union[CharityProject, Donation],
    session: AsyncSession,
) -> Union[CharityProject, Donation]:
    """
    Функция проводит распределение не инвестированных
    денежных средств по не закрытым проектам,
    если создается новое пожертвование или проект.
    """
    full_new_obj_amount = new_obj.full_amount
    if new_obj.invested_amount is not None:
        invested_new_obj_amount = new_obj.invested_amount
    else:
        invested_new_obj_amount = 0
    uninvested_db_obj = await session.execute(
        select(uninvested_obj_model).where(
            uninvested_obj_model.fully_invested.is_(False)
        )
    )
    uninvested_db_obj = uninvested_db_obj.scalars().all()

    for db_obj in uninvested_db_obj:
        uninvested_db_obj_amount = db_obj.full_amount - db_obj.invested_amount
        uninvested_new_obj_amount = (
            full_new_obj_amount - invested_new_obj_amount
        )
        if uninvested_new_obj_amount == 0:
            break
        invested_db_obj_amount = db_obj.invested_amount
        if uninvested_db_obj_amount > uninvested_new_obj_amount:
            invested_db_obj_amount += uninvested_new_obj_amount
            invested_new_obj_amount += uninvested_new_obj_amount
        elif uninvested_db_obj_amount <= uninvested_new_obj_amount:
            invested_db_obj_amount += uninvested_db_obj_amount
            invested_new_obj_amount += uninvested_db_obj_amount
            setattr(db_obj, "fully_invested", True)
            setattr(db_obj, "close_date", datetime.now())
        setattr(db_obj, "invested_amount", invested_db_obj_amount)
        session.add(db_obj)
    setattr(new_obj, "invested_amount", invested_new_obj_amount)
    if full_new_obj_amount == invested_new_obj_amount:
        setattr(new_obj, "fully_invested", True)
        setattr(new_obj, "close_date", datetime.now())
    session.add(new_obj)
    await session.commit()
    await session.refresh(new_obj)
    return new_obj
