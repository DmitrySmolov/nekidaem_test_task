import logging

from fastapi import FastAPI

from app.api.api_v1.routers import main_router
from app.config import settings

logging.basicConfig(
    level=logging.INFO,
    format=settings.logging_format,
    datefmt=settings.logging_dt_format
)

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description
)

app.include_router(main_router)
