from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

DATABASE_URL = settings.database_url

engine = create_async_engine(DATABASE_URL)

AsyncSesssionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
