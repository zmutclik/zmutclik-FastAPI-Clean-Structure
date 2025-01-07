import os

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    APP_NAME: str = "FastAPI cleanStructure"
    APP_DESCRIPTION: str = "This is a very fancy project, with auto docs for the API and everything."
    APP_VERSION: str = "init"
    ENV: str = "development"
    DEBUG: bool = True
    APP_HOST: str = "localhost"
    APP_PORT: int = 8016
    DBAPPS_URL: str = f"mysql+aiomysql://fastapi:fastapi@localhost:3306/db"
    DBCORE_URL: str = f"mysql+aiomysql://fastapi:fastapi@localhost:3306/db"
    DBLOGS_URL: str = f"mysql+aiomysql://fastapi:fastapi@localhost:3306/db"
    JWT_SECRET_KEY: str = "fastapi"
    JWT_ALGORITHM: str = "HS256"
    CELERY_BROKER_URL: str = "amqp://user:bitnami@localhost:5672/"
    CLIENT_KEY: str = "fastapi-clean-structure_client"
    COOKIES_KEY: str = "fastapi-clean-structure_token"
    COOKIES_EXPIRED: int = 30


class DevelopmentConfig(Config):
    DBAPPS_URL: str = f"mysql+aiomysql://root:fastapi@db:3306/db"


class LocalConfig(Config):
    DBAPPS_URL: str = f"mysql+aiomysql://root:blackant@192.168.80.11:3307/db"
    DBCORE_URL: str = f"mysql+aiomysql://root:blackant@192.168.80.11:3307/db"
    DBLOGS_URL: str = f"mysql+aiomysql://root:blackant@192.168.80.11:3307/db"


class ProductionConfig(Config):
    DEBUG: bool = False
    DBAPPS_URL: str = f"mysql+aiomysql://fastapi:fastapi@localhost:3306/db"
    DBAPPS_URL: str = f"mysql+aiomysql://fastapi:fastapi@localhost:3306/db"
    DBAPPS_URL: str = f"mysql+aiomysql://fastapi:fastapi@localhost:3306/db"


def get_config() -> Config:
    env = os.getenv("ENV", "local")
    config_type = {
        "development": DevelopmentConfig(),
        "local": LocalConfig(),
        "production": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()
