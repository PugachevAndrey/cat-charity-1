from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate
)


class CRUDCharityProject(CRUDBase[
    CharityProject,
    CharityProjectCreate,
    CharityProjectUpdate
]):
    """CRUD-операции для модели CharityProject."""

    async def get_project_by_name(
        self,
        name: str,
        session: AsyncSession,
    ) -> CharityProject | None:
        """
        Получить проект по его имени.

        Возвращает объект проекта или None, если проект не найден.
        """
        result = await session.execute(
            select(self.model).where(self.model.name == name)
        )
        return result.scalar_one_or_none()

    async def get_open_projects(
        self,
        session: AsyncSession,
    ) -> list[CharityProject]:
        """
        Получить список открытых (не полностью проинвестированных) проектов.

        Сортировка по дате создания (старые раньше).
        """
        result = await session.execute(
            select(self.model)
            .where(self.model.fully_invested.is_(False))
            .order_by(self.model.create_date)
        )
        return result.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
