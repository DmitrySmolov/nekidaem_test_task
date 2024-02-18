import logging

from fastapi import FastAPI, Query
from fastapi_pagination import add_pagination, Page

from app.api.api_v1.routers import main_router
from app.config import constants, settings

logging.basicConfig(
    level=logging.INFO,
    format=settings.logging_format,
    datefmt=settings.logging_dt_format
)

Page = Page.with_custom_options(
    size=Query(
        constants.POSTS_PER_PAGE,
        ge=1,
        le=constants.MAX_POSTS_IN_FEED
    )
)

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description
)

add_pagination(app)

app.include_router(main_router)
