from typing import Optional
from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.charityproject import charity_project_crud
from app.models.charity_project import CharityProject


async def check_name_duplicate(name, session: AsyncSession) -> None:
    duplicate = await charity_project_crud.get_obj_by_name(name, session)
    if duplicate:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            "Проект с таким именем уже существует!",
        )


async def check_project_exist(project_id: int, session: AsyncSession):
    project = await charity_project_crud.get(project_id, session)
    if not project:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Проект не существует!")
    return project


async def check_project_before_edit(
    project: CharityProject,
    new_full_amount: Optional[int] = None,
) -> None:
    if project.fully_invested:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            "Закрытый проект нельзя редактировать!",
        )
    if new_full_amount is not None:
        if new_full_amount < project.invested_amount:
            raise HTTPException(
                HTTPStatus.BAD_REQUEST,
                "Общяя стоимость проекта не может \
                    быть изменена в меньшую сторону!",
            )
    return project


async def check_project_before_delete(project: CharityProject) -> None:
    if project.fully_invested:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            "В проект были внесены средства, не подлежит удалению!",
        )
    if project.invested_amount > 0:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            "В проект были внесены средства, не подлежит удалению!",
        )
