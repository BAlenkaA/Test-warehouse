from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str
    db_user: str
    db_password: str
    db_name: str
    db_port: str
    db_host: str
    db_user_test: str
    db_password_test: str
    db_name_test: str
    db_port_test: str
    db_host_test: str

    class Config:
        env_file = '.env'


settings = Settings()
