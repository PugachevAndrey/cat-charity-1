from sqlalchemy import Column, Text, Integer

from app.models.base import InvestmentBase


class Donation(InvestmentBase):
    """
    Модель пожертвования.

    Хранит информацию о пожертвовании: сумма, комментарий,
    распределённая сумма, статус, даты создания и закрытия.
    """

    __tablename__ = "donation"

    comment = Column(Text, nullable=True)
    full_amount = Column(Integer, nullable=False)
