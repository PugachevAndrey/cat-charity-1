from sqlalchemy import Column, String, Text, Integer

from app.models.base import InvestmentBase


class CharityProject(InvestmentBase):
    """
    Модель целевого проекта благотворительного фонда.

    Хранит информацию о проекте: название, описание, требуемую сумму,
    собранную сумму, статус сбора, даты создания и закрытия.
    """

    __tablename__ = "charityproject"

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    full_amount = Column(Integer, nullable=False)
