from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Основные настройки приложения."""
    app_title: str = 'NeKidaem'
    app_description: str = 'NeKidaem API'
    database_url: str = (
        'postgresql+asyncpg://postgres:postgres@db:5432/nekidaem'
    )
    logging_format: str = '%(asctime)s - %(levelname)s - %(message)s'
    logging_dt_format: str = '%Y-%m-%d %H:%M:%S'
    redis_url: str = 'redis://broker:6379/0'

    class Config:
        env_file = '.env'
        extra = 'ignore'


settings = Settings()


class Constants:
    """Константы приложения."""
    TITLE_MAX_LENGTH = 50
    CONTENT_MAX_LENGTH = 140
    EMAIL_MAX_LENGTH = 254
    POSTS_PER_PAGE = 10
    MAX_POSTS_IN_FEED = 500
    POSTS_PER_EMAIL = 5
    MAILING_TIME = (12, 00)  # (hour, minute)


constants = Constants()
