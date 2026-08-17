from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Boolean


from app.core.db import Base


class InvestmentBase(Base):
    """
    Абстрактная базовая модель для сущностей с инвестициями.

    Содержит общие поля для моделей CharityProject и Donation:
    id, invested_amount, fully_invested, create_date, close_date.
    """

    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, nullable=True)
