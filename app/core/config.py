from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str
    db_user: str
    db_password: str
    db_name: str
    db_port: str
    db_host: str

    class Config:
        env_file = '.env'


settings = Settings()
