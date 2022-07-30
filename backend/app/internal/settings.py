from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    instagram_account_username: str
    instagram_account_password: str
    redis_endpoint: str
    redis_password: str
    redis_port: int

    class Config:
        env_file = "internal/.env"


@lru_cache()
def get_settings():
    return Settings()
