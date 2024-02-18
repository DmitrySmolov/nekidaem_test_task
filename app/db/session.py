from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

DATABASE_URL = settings.database_url

engine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Возвращает асинхронную сессию для работы с БД."""
    async with AsyncSessionLocal() as session:
        yield session
