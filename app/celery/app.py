import asyncio

from celery import Celery

from app.celery.services import send_email_to_users_with_feed
from app.config import settings

celery_app = Celery(
    main='celery_app',
    broker=settings.redis_url
)


@celery_app.task
def email_users_with_feed():
    """
    Рассылка емэйлов (понарошку) пользователям с новыми постами из ленты.
    """
    asyncio.run(send_email_to_users_with_feed())
