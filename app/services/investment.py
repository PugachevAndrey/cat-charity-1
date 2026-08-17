from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud


async def invest(session: AsyncSession) -> None:
    """
    Распределить неинвестированные пожертвования по открытым проектам.

    Логика:
    - Получает все не полностью проинвестированные пожертвования.
    - Получает все открытые проекты.
    - Идёт по проектам в порядке их создания (старые раньше).
    - Для каждого проекта берёт пожертвования по очереди и инвестирует
      сумму, необходимую для закрытия проекта или до исчерпания пожертвования.
    - Если пожертвование полностью использовано – закрывает его.
    - Если проект собрал нужную сумму – закрывает его.
    """
    donations = await donation_crud.get_uninvested_donations(session)
    projects = await charity_project_crud.get_open_projects(session)

    if not donations or not projects:
        return

    for project in projects:
        for donation in donations:
            if donation.fully_invested:
                continue

            available_donation = (
                donation.full_amount - donation.invested_amount
            )
            if available_donation <= 0:
                donation.fully_invested = True
                donation.close_date = datetime.now()
                continue

            need = project.full_amount - project.invested_amount
            if need <= 0:
                project.fully_invested = True
                project.close_date = datetime.now()
                break

            invested = min(available_donation, need)
            donation.invested_amount += invested
            project.invested_amount += invested

            if donation.invested_amount >= donation.full_amount:
                donation.fully_invested = True
                donation.close_date = datetime.now()

            if project.invested_amount >= project.full_amount:
                project.fully_invested = True
                project.close_date = datetime.now()
                break
