from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from sqlalchemy.orm import declarative_base

from app.core.config import settings

engine = create_async_engine(settings.database_url, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Генератор асинхронной сессии базы данных.

    Создаёт сессию через AsyncSessionLocal и возвращает её,
    автоматически закрывая после завершения контекста.
    """
    async with AsyncSessionLocal() as session:
        yield session
