from fastapi import Query
from fastapi_pagination import Page

from app.config import constants

CustomPage = Page.with_custom_options(
    size=Query(
        constants.POSTS_PER_PAGE,
        ge=1,
        le=constants.MAX_POSTS_IN_FEED
    )
)
