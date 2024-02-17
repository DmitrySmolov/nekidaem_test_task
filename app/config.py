from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Основные настройки приложения."""
    app_title: str = 'NeKidaem'
    app_description: str = 'NeKidaem API'
    database_url: str = (
        'postgresql+asyncpg://nekidaem:nekidaem@localhost/nekidaem'
    )
    logging_format: str = '%(asctime)s - %(levelname)s - %(message)s'
    logging_dt_format: str = '%Y-%m-%d %H:%M:%S'

    class Config:
        env_file = '.env'


settings = Settings()


class Constants:
    """Константы приложения."""
    # Пользовательские роли
    TITLE_MAX_LENGTH = 50
    CONTENT_MAX_LENGTH = 140
    EMAIL_MAX_LENGTH = 254
    POSTS_PER_PAGE = 10
    MAX_POSTS_IN_FEED = 500


constants = Constants()
