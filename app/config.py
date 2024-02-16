from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'NeKidaem'
    app_description: str = 'NeKidaem API'
    database_url: str = 'postgresql://nekidaem:nekidaem@localhost/nekidaem'
    logging_format: str = '%(asctime)s - %(levelname)s - %(message)s'
    logging_dt_format: str = '%Y-%m-%d %H:%M:%S'

    class Config:
        env_file = '.env'


settings = Settings()
