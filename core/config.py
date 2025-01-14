import os
import sqlite3
from pydantic_settings import BaseSettings


DB_FILE = ".db/system/core.db"
DB_ENGINE = "sqlite:///" + DB_FILE
repository_db = ""
repository_rmq = ""
version_name = "null" 

if os.path.exists(DB_FILE):
    file_stats = os.stat(DB_FILE)
    if file_stats.st_size != 0:
        with sqlite3.connect(".db/system/core.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

        cursor.execute("SELECT * FROM repository where allocation='DBAPPS_URL_DEFAULT' and is_active='1' ORDER BY id DESC LIMIT 1")
        _r = cursor.fetchone()
        if _r:
            repository_db = _r["datalink"].format(user=_r["user"], password=_r["password"])
            
        cursor.execute("SELECT * FROM repository where allocation='RabbitMQ' and is_active='1' ORDER BY id DESC LIMIT 1")
        _r = cursor.fetchone()
        if _r:
            repository_rmq = _r["datalink"].format(user=_r["user"], password=_r["password"])
            
        cursor.execute("SELECT * FROM changelog ORDER BY dateupdate DESC LIMIT 1")
        _r = cursor.fetchone()
        if _r:
            version_name = _r["version_name"]


class Config(BaseSettings):
    APP_NAME: str = "FastAPI cleanStructure"
    APP_DESCRIPTION: str = "This is a very fancy project, with auto docs for the API and everything."
    APP_VERSION: str = version_name
    ENV: str = "development"
    DEBUG: bool = True
    APP_HOST: str = "localhost"
    APP_PORT: int = 8016
    DBAPPS_URL: str = repository_db
    CELERY_BROKER_URL: str = repository_rmq
    JWT_SECRET_KEY: str = "fastapi"
    JWT_ALGORITHM: str = "HS512"
    CLIENT_KEY: str = "fastapi-clean-structure_client"
    COOKIES_KEY: str = "fastapi-clean-structure_token"
    COOKIES_EXPIRED: int = 30


config: Config = Config()
