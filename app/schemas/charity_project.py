from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class CharityProjectBase(BaseModel):
    """
    Базовая схема целевого проекта.

    Содержит основные поля: name, description, full_amount.
    Используется как основа для создания и отображения.
    """

    model_config = ConfigDict(extra="forbid")
    name: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=10)
    full_amount: int = Field(..., gt=0)


class CharityProjectCreate(CharityProjectBase):
    """Схема для создания нового целевого проекта."""


class CharityProjectUpdate(BaseModel):
    """
    Схема для обновления целевого проекта.

    Все поля опциональны. Запрещены дополнительные поля.
    """

    model_config = ConfigDict(extra="forbid")
    name: str | None = Field(None, min_length=5, max_length=100)
    description: str | None = Field(None, min_length=10)
    full_amount: int | None = Field(None, gt=0)


class CharityProjectDB(CharityProjectBase):
    """
    Схема для отображения целевого проекта из базы данных.

    Включает служебные поля: id, invested_amount, fully_invested,
    create_date, close_date.
    """

    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime | None

    model_config = ConfigDict(from_attributes=True)
