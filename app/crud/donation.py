from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.schemas.donation import DonationCreate
from pydantic import BaseModel


class CRUDDonation(CRUDBase[Donation, DonationCreate, BaseModel]):
    """
    CRUD-операции для модели Donation.
    """

    async def get_uninvested_donations(
        self,
        session: AsyncSession,
    ) -> list[Donation]:
        """
        Получить список не полностью проинвестированных пожертвований.

        Сортировка по дате создания (старые раньше).
        """
        result = await session.execute(
            select(self.model)
            .where(self.model.fully_invested.is_(False))
            .order_by(self.model.create_date)
        )
        return result.scalars().all()


donation_crud = CRUDDonation(Donation)
