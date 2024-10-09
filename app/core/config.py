from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str
    db_user: str
    db_password: str
    db_name: str
    db_port: int
    db_host: str
    mode: str

    model_config = ConfigDict(
        env_file='.env'
    )


settings = Settings()

DATABASE_URL = (f'postgresql+asyncpg://{settings.db_user}:'
                f'{settings.db_password}@{settings.db_host}:'
                f'{settings.db_port}/{settings.db_name}')
