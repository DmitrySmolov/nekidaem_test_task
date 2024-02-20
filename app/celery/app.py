import asyncio

from celery import Celery
from celery.schedules import crontab

from app.celery.tasks import send_email_to_users_with_feed
from app.config import constants, settings

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


celery_app.conf.beat_schedule = {
    'email_uesrs_with_feed_daily': {
        'task': 'app.celery.app.email_users_with_feed',
        'schedule': crontab(
            hour=constants.MAILING_TIME[0],
            minute=constants.MAILING_TIME[1]
        ),
    },
}
