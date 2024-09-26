from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str
    db_user: str
    db_password: str
    db_name: str
    db_port: str
    db_host: str
    # переменные для тестовой базы
    db_user_test: str
    db_password_test: str
    db_name_test: str
    db_port_test: str
    db_host_test: str

    model_config = ConfigDict(
        env_file='.env'
    )


settings = Settings()
