from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationCreateResponse
)
from app.services.investment import invest

router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.post("/", response_model=DonationCreateResponse)
async def create_donation(
    donation_create: DonationCreate,
    session: SessionDep,
) -> DonationCreateResponse:
    """
    Создать новое пожертвование.

    - Сохраняет пожертвование в БД.
    - Запускает процесс инвестирования свободных средств в открытые проекты.
    - Возвращает созданное пожертвование без служебных полей
      (invested_amount, fully_invested, close_date).
    """
    new_donation = await donation_crud.create(donation_create, session)
    await invest(session)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get("/", response_model=list[DonationDB])
async def get_all_donations(
    session: SessionDep,
) -> list[DonationDB]:
    """
    Получить список всех пожертвований.

    Возвращает все пожертвования с полной информацией,
    включая служебные поля (invested_amount, fully_invested, close_date).
    """
    donations = await donation_crud.get_multi(session)
    return donations
