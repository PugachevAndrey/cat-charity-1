from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
    CharityProjectDB,
)
from app.api.validators import check_name_duplicate, check_project_before_edit
from app.services.investment import invest
from app.core.constants import (
    HTTP_400_BAD_REQUEST,
    ERROR_PROJECT_HAS_INVESTMENTS,
    ERROR_FULL_AMOUNT_LESS_THAN_INVESTED,
)

router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.post("/", response_model=CharityProjectDB)
async def create_project(
    project_in: CharityProjectCreate,
    session: SessionDep,
) -> CharityProjectDB:
    """
    Создать новый целевой проект.

    - Проверяет уникальность имени.
    - Создаёт проект в БД.
    - Запускает процесс инвестирования свободных пожертвований.
    - Возвращает созданный проект с обновлёнными полями.
    """
    await check_name_duplicate(project_in.name, session)
    new_project = await charity_project_crud.create(project_in, session)
    await invest(session)
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.get("/", response_model=list[CharityProjectDB])
async def get_all_projects(
    session: SessionDep,
) -> list[CharityProjectDB]:
    """
    Получить список всех целевых проектов.

    Возвращает все проекты, включая закрытые.
    """
    projects = await charity_project_crud.get_multi(session)
    return projects


@router.patch("/{project_id}", response_model=CharityProjectDB)
async def update_project(
    project_id: int,
    project_update: CharityProjectUpdate,
    session: SessionDep,
) -> CharityProjectDB:
    """
    Обновить данные целевого проекта.

    - Проверяет, что проект существует и не закрыт.
    - Если изменяется имя – проверяет уникальность.
    - Запрещает установку `full_amount` меньше уже внесённой суммы.
    - Если после обновления `full_amount <= invested_amount`– закрывает проект.
    """
    project = await check_project_before_edit(project_id, session)

    if project_update.name is not None:
        await check_name_duplicate(project_update.name, session)

    if (
        project_update.full_amount is not None
        and project_update.full_amount < project.invested_amount
    ):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=ERROR_FULL_AMOUNT_LESS_THAN_INVESTED,
        )

    updated = await charity_project_crud.update(
        project,
        project_update,
        session
    )

    if updated.invested_amount >= updated.full_amount:
        updated.fully_invested = True
        updated.close_date = datetime.now()
        session.add(updated)

    await session.commit()
    await session.refresh(updated)
    return updated


@router.delete("/{project_id}", response_model=CharityProjectDB)
async def delete_project(
    project_id: int,
    session: SessionDep,
) -> CharityProjectDB:
    """
    Удалить целевой проект.

    - Проверяет, что проект существует и не закрыт.
    - Запрещает удаление, если в проект уже были инвестированы средства.
    """
    project = await check_project_before_edit(project_id, session)

    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=ERROR_PROJECT_HAS_INVESTMENTS,
        )

    deleted = await charity_project_crud.remove(project, session)
    return deleted
