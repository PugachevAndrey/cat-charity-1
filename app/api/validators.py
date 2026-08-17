from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.core.constants import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    ERROR_PROJECT_NAME_EXISTS,
    ERROR_PROJECT_NOT_FOUND,
    ERROR_PROJECT_CLOSED,
    ERROR_DONATION_NOT_FOUND,
)


async def check_name_duplicate(
    name: str,
    session: AsyncSession,
) -> None:
    """
    Проверить, что имя проекта не занято.

    Если проект с таким именем уже существует, выбрасывает исключение 400.
    """
    project = await charity_project_crud.get_project_by_name(name, session)
    if project:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=ERROR_PROJECT_NAME_EXISTS,
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """
    Проверить, что проект существует.

    Если проект не найден, выбрасывает исключение 404.
    Возвращает объект проекта.
    """
    project = await charity_project_crud.get(project_id, session)
    if not project:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=ERROR_PROJECT_NOT_FOUND,
        )
    return project


async def check_project_before_edit(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """
    Проверить, что проект существует и не закрыт.

    Если проект закрыт, выбрасывает исключение 400.
    Возвращает объект проекта.
    """
    project = await check_project_exists(project_id, session)
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=ERROR_PROJECT_CLOSED,
        )
    return project


async def check_donation_exists(
    donation_id: int,
    session: AsyncSession,
) -> Donation:
    """
    Проверить, что пожертвование существует.

    Если пожертвование не найдено, выбрасывает исключение 404.
    Возвращает объект пожертвования.
    """
    donation = await donation_crud.get(donation_id, session)
    if not donation:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=ERROR_DONATION_NOT_FOUND,
        )
    return donation
