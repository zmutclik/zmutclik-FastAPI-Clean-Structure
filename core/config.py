import os
from pydantic_settings import BaseSettings
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Table, MetaData, select

DBCORE_FILE = ".db/system/core.db"
DBCORE_ENGINE = "sqlite+aiosqlite:///" + DBCORE_FILE
dbcore_engine = create_engine(DBCORE_ENGINE.replace("+aiosqlite", ""))

DBAUTH_FILE = ".db/system/auth.db"
DBAUTH_ENGINE = "sqlite+aiosqlite:///" + DBAUTH_FILE
dbauth_engine = create_engine(DBAUTH_ENGINE.replace("+aiosqlite", ""))

DBMENU_FILE = ".db/system/menu.db"
DBMENU_ENGINE = "sqlite+aiosqlite:///" + DBMENU_FILE
dbmenu_engine = create_engine(DBMENU_ENGINE.replace("+aiosqlite", ""))


#######################################################################################################################
if os.path.exists(DBCORE_FILE):
    file_stats = os.stat(DBCORE_FILE)
    if file_stats.st_size != 0:
        metadata = MetaData()
        repo_table = Table("repository", metadata, autoload_with=dbcore_engine)
        vers_table = Table("changelog", metadata, autoload_with=dbcore_engine)
        core_table = Table("coresystem", metadata, autoload_with=dbcore_engine)
        origin_table = Table("cross_origin", metadata, autoload_with=dbcore_engine)


def get_repository(allocation: str):
    return (
        select(repo_table)
        .where(repo_table.c.deleted_at == None, repo_table.c.allocation == allocation, repo_table.c.is_active == True)
        .order_by(repo_table.c.id.desc())
    )


repository_db = ""
repository_mql = ""
version_name = "zero"
allow_origins = []
configdefault = {
    "environment": "local",
    "app_name": "FastAPI cleanStructure",
    "app_desc": "This is a very fancy project, with auto docs for the API and everything.",
    "app_host": "127.0.0.1",
    "app_port": 8016,
    "jwt_scret_key": "fastapi",
    "jwt_algorithm": "HS512",
    "prefix_session": "fastapi-clean-structure_",
    "cookies_exp": 30,
    "refresh_exp": 60 * 8,
    "debug": True,
}

if os.path.exists(DBCORE_FILE):
    file_stats = os.stat(DBCORE_FILE)
    if file_stats.st_size != 0:
        with dbcore_engine.begin() as connection:
            with Session(bind=connection) as db:
                for item in db.execute(get_repository("DBAPPS_URL_DEFAULT")):
                    repository_db = item.datalink.format(user=item.user, password=item.password)
                for item in db.execute(get_repository("RabbitMQ")):
                    repository_mql = item.datalink.format(user=item.user, password=item.password)
                stmt = select(vers_table).limit(1).order_by(vers_table.c.id.desc())
                for item in db.execute(stmt):
                    version_name = item.version_name
                stmt = select(core_table).limit(1)
                for item in db.execute(stmt):
                    configdefault = item._mapping
                result = db.execute(select(origin_table.c.link).where(origin_table.c.deleted_at == None))
                allow_origins = [item.link for item in result]
                if allow_origins == []:
                    allow_origins.append("*")


class Config(BaseSettings):
    APP_NAME: str = configdefault["app_name"]
    APP_DESCRIPTION: str = configdefault["app_desc"]
    APP_VERSION: str = version_name
    ENV: str = configdefault["environment"]
    DEBUG: bool = configdefault["debug"]
    APP_HOST: str = configdefault["app_host"]
    APP_PORT: int = configdefault["app_port"]
    DBAPPS_URL: str = repository_db
    CELERY_BROKER_URL: str = repository_mql
    JWT_SECRET_KEY: str = configdefault["jwt_scret_key"]
    JWT_ALGORITHM: str = configdefault["jwt_algorithm"]
    PREFIX_KEY: str = configdefault["prefix_session"]
    CLIENT_KEY: str = configdefault["prefix_session"] + "client"
    COOKIES_KEY: str = configdefault["prefix_session"] + "token"
    REFRESH_KEY: str = configdefault["prefix_session"] + "refresh"
    COOKIES_EXPIRED: int = configdefault["cookies_exp"]
    REFRESH_EXPIRED: int = configdefault["refresh_exp"]
    ALLOW_ORIGINS: list[str] = allow_origins


config: Config = Config()
