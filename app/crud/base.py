from typing import TypeVar, Generic, Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from app.core.db import Base

ModelType = TypeVar("ModelType", bound=Base)  # type: ignore
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Базовый класс для CRUD-операций.

    Предоставляет стандартные методы для работы с моделями SQLAlchemy:
    get, get_multi, create, update, remove.
    """

    def __init__(self, model: Type[ModelType]):
        """Сохраняет модель, с которой работает CRUD."""
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ) -> ModelType | None:
        """
        Получить объект по его ID.

        Возвращает объект модели или None, если не найден.
        """
        result = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return result.scalar_one_or_none()

    async def get_multi(
        self,
        session: AsyncSession,
    ) -> list[ModelType]:
        """Получить список всех объектов модели."""
        result = await session.execute(select(self.model))
        return result.scalars().all()

    async def create(
        self,
        obj_create: CreateSchemaType,
        session: AsyncSession,
    ) -> ModelType:
        """
        Создать новый объект в базе.

        Принимает схему создания, преобразует в словарь и создаёт модель.
        Выполняет flush, чтобы получить ID, но не коммитит.
        """
        obj_data = obj_create.model_dump()
        db_obj = self.model(**obj_data)
        session.add(db_obj)
        await session.flush()
        return db_obj

    async def update(
        self,
        db_obj: ModelType,
        obj_update: UpdateSchemaType | dict,
        session: AsyncSession,
    ) -> ModelType:
        """
        Обновить существующий объект.

        Принимает словарь или Pydantic-схему с обновляемыми полями.
        Обновляет только переданные поля.
        Выполняет flush, но не коммитит.
        """
        if isinstance(obj_update, dict):
            update_data = obj_update
        else:
            update_data = obj_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        session.add(db_obj)
        await session.flush()
        return db_obj

    async def remove(
        self,
        db_obj: ModelType,
        session: AsyncSession,
    ) -> ModelType:
        """
        Удалить объект из базы.

        Выполняет commit, так как удаление должно быть окончательным.
        """
        await session.delete(db_obj)
        await session.commit()
        return db_obj
