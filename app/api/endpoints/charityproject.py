from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from app.crud.charityproject import charity_project_crud
from app.core.user import current_superuser
from app.models.donation import Donation
from app.models.charity_project import CharityProject
from app.schemas.charityproject import (
    CharityProjectCreate,
    CharityProjectUpdate,
    CharityProjectDB,
)
from app.servises.investing import check_uninvested_amounts
from app.api.validators import (
    check_name_duplicate,
    check_project_before_edit,
    check_project_exist,
    check_project_before_delete,
)


router = APIRouter()


@router.get(
    "/",
    response_model=List[CharityProjectDB],
    response_model_exclude={"close_date"},
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session),
) -> List[CharityProject]:
    return await charity_project_crud.get_all(session)


@router.post(
    "/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=(Depends(current_superuser),),
)
async def create_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    await check_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(project, session)
    return await check_uninvested_amounts(Donation, new_project, session)


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=(Depends(current_superuser),),
)
async def remove_charity_project(
    project_id: int, session: AsyncSession = Depends(get_async_session)
) -> CharityProject:
    project = await check_project_exist(project_id, session)
    await check_project_before_delete(project)
    return await charity_project_crud.remove(project, session)


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=(Depends(current_superuser),),
)
async def update_charity_project(
    project_id: int,
    updated_project: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    project = await check_project_exist(project_id, session)
    await check_project_before_edit(
        project,
        new_full_amount=updated_project.full_amount,
    )
    if updated_project.name is not None:
        await check_name_duplicate(updated_project.name, session)
    project = await charity_project_crud.update(
        project, updated_project, session
    )
    if updated_project.full_amount is not None:
        return await check_uninvested_amounts(Donation, project, session)
    return project
