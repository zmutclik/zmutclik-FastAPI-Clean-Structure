import os

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True
    APP_HOST: str = "localhost"
    APP_PORT: int = 8016
    DB_URL: str = f"mysql+aiomysql://fastapi:fastapi@localhost:3306/db"
    JWT_SECRET_KEY: str = "fastapi"
    JWT_ALGORITHM: str = "HS256"
    CELERY_BROKER_URL: str = "amqp://user:bitnami@localhost:5672/"


class DevelopmentConfig(Config):
    DB_URL: str = f"mysql+aiomysql://root:fastapi@db:3306/db"


class LocalConfig(Config):
    DB_URL: str = f"mysql+aiomysql://fastapi:fastapi@localhost:3307/db"


class ProductionConfig(Config):
    DEBUG: bool = False
    DB_URL: str = f"mysql+aiomysql://fastapi:fastapi@localhost:3306/db"


def get_config() -> Config:
    env = os.getenv("ENV", "local")
    print("")
    print("ENV = ", env)
    print("")
    config_type = {
        "development": DevelopmentConfig(),
        "local": LocalConfig(),
        "production": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()
