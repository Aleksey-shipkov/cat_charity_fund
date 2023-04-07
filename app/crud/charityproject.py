from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_obj_by_name(self, name: str, session: AsyncSession):
        db_obj = await session.execute(
            select(CharityProject).where(CharityProject.name == name)
        )
        return db_obj.scalars().first()


charity_project_crud = CRUDCharityProject(CharityProject)
