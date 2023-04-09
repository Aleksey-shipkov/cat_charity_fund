from typing import Optional, List, TypeVar, Generic, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.encoders import jsonable_encoder
from app.models.user import User

T = TypeVar("T")


class CRUDBase(Generic[T]):
    def __init__(self, model: T) -> None:
        self.model = model

    async def get(self, obj_id: int, session: AsyncSession) -> T:
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_all(self, session: AsyncSession) -> List[T]:
        db_obj = await session.execute(select(self.model))
        return db_obj.scalars().all()

    async def create(
        self, obj_in: Any, session: AsyncSession, user: Optional[User] = None
    ) -> T:
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data["user_id"] = user.id
        new_obj = self.model(**obj_in_data)
        session.add(new_obj)
        await session.commit()
        await session.refresh(new_obj)
        return new_obj

    async def update(self, db_obj: T, obj_in: Any, session: AsyncSession) -> T:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(self, db_obj: T, session: AsyncSession) -> T:
        await session.delete(db_obj)
        await session.commit()
        return db_obj
