from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class DonationBase(BaseModel):
    """
    Базовая схема пожертвования.

    Содержит обязательное поле full_amount и опциональное comment.
    Используется как основа для создания и отображения.
    """

    model_config = ConfigDict(extra="forbid")
    full_amount: int = Field(..., gt=0)
    comment: str | None = None


class DonationCreate(DonationBase):
    """Схема для создания нового пожертвования."""


class DonationCreateResponse(BaseModel):
    """
    Схема для ответа при создании пожертвования.

    Возвращает только пользовательские поля, без служебных
    (invested_amount, fully_invested, close_date).
    """

    full_amount: int
    comment: str | None = None
    id: int
    create_date: datetime

    model_config = ConfigDict(from_attributes=True)


class DonationDB(DonationBase):
    """
    Полная схема для чтения пожертвований из базы данных.

    Включает все поля, включая служебные:
    id, invested_amount, fully_invested, create_date, close_date.
    """

    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime | None

    model_config = ConfigDict(from_attributes=True)
