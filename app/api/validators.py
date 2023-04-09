from typing import Optional
from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.charityproject import charity_project_crud
from app.models.charity_project import CharityProject


class Error:
    PROJECT_ALREADY_EXIST = "Проект с таким именем уже существует!"
    PROJECT_NOT_EXIST = "Проект не существует!"
    CLOSED_PROJECT_NOT_CHANGEBLE = "Закрытый проект нельзя редактировать!"
    PROJECT_FULL_AMOUNT_CHANGE = (
        "Общяя стоимость проекта не может быть изменена в меньшую сторону!"
    )
    INVESTED_PROJECT_NOT_DELETED = (
        "В проект были внесены средства, не подлежит удалению!"
    )


async def check_name_duplicate(name: str, session: AsyncSession) -> None:
    duplicate = await charity_project_crud.get_obj_by_name(name, session)
    if duplicate:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            Error.PROJECT_ALREADY_EXIST,
        )


async def check_project_exist(
    project_id: int, session: AsyncSession
) -> Optional[CharityProject]:
    project = await charity_project_crud.get(project_id, session)
    if not project:
        raise HTTPException(HTTPStatus.NOT_FOUND, Error.PROJECT_NOT_EXIST)
    return project


async def check_project_before_edit(
    project: CharityProject,
    new_full_amount: Optional[int] = None,
) -> None:
    if project.fully_invested:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            Error.CLOSED_PROJECT_NOT_CHANGEBLE,
        )
    if new_full_amount is None:
        return project
    if new_full_amount < project.invested_amount:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            Error.PROJECT_FULL_AMOUNT_CHANGE,
        )


async def check_project_before_delete(project: CharityProject) -> None:
    if project.fully_invested:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            Error.INVESTED_PROJECT_NOT_DELETED,
        )
    if project.invested_amount > 0:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            Error.INVESTED_PROJECT_NOT_DELETED,
        )
