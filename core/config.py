import os
from typing import Optional, Dict
from pydantic import BaseModel
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

DBSECURITY_FILE = ".db/system/security.db"
DBSECURITY_ENGINE = "sqlite+aiosqlite:///" + DBSECURITY_FILE
dbsecurity_engine = create_engine(DBSECURITY_ENGINE.replace("+aiosqlite", ""))


class RepositoryModel(BaseModel):
    datalink: str
    name: Optional[str] = None
    user: Optional[str] = None


#######################################################################################################################
if os.path.exists(DBCORE_FILE):
    file_stats = os.stat(DBCORE_FILE)
    if file_stats.st_size != 0:
        metadata = MetaData()
        repo_table = Table("repository", metadata, autoload_with=dbcore_engine)
        vers_table = Table("changelog", metadata, autoload_with=dbcore_engine)
        auth_table = Table("authconfig", metadata, autoload_with=dbcore_engine)
        core_table = Table("coresystem", metadata, autoload_with=dbcore_engine)
        origin_table = Table("cross_origin", metadata, autoload_with=dbcore_engine)


def get_repository(allocation: str):
    return (
        select(repo_table)
        .where(
            repo_table.c.deleted_at == None,
            repo_table.c.allocation == allocation,
            repo_table.c.is_active == True,
        )
        .order_by(repo_table.c.id.desc())
    )


repository = {}
version_name = "zero"
allow_origins = []
configdefault = {
    "environment": "local",
    "app_name": "FastAPI cleanStructure",
    "app_desc": "This is a very fancy project, with auto docs for the API and everything.",
    "app_host": "127.0.0.1",
    "app_port": 8016,
    "host_url": "http://172.0.0.1:8016",
    "debug": True,
}
authconfigdefault = {
    "sso_login_url": "http://",
    "sso_token_url": "http://",
    "sso_client_id": "",
    "jwt_scret_key": "fastapi",
    "jwt_algorithm": "HS512",
    "cookies_prefix": "fastapi-clean-structure_",
    "cookies_https": False,
    "cookies_exp": 15,
    "refresh_exp": 60 * 8,
    "timeout_exp": 30,
    "register_account": True,
    "login_by_otp": False,
}

if os.path.exists(DBCORE_FILE):
    file_stats = os.stat(DBCORE_FILE)
    if file_stats.st_size != 0:
        with dbcore_engine.begin() as connection:
            with Session(bind=connection) as db:
                stmt = (
                    select(repo_table)
                    .where(
                        repo_table.c.deleted_at.is_(None),
                        repo_table.c.is_active.is_(True),
                    )
                    .order_by(repo_table.c.id.desc())
                )
                for item in db.execute(stmt).fetchall():
                    repository[item.allocation] = RepositoryModel(
                        datalink=item.datalink.format(user=item.user or "", password=item.password or ""),
                        user=item.user,
                        name=item.name,
                    )

                stmt = select(vers_table).order_by(vers_table.c.id.desc()).limit(1)
                item = db.execute(stmt).fetchone()
                version_name = item.version_name if item else None

                stmt = select(core_table)
                item = db.execute(stmt).fetchone()
                configdefault = item._mapping if item else None

                stmt = select(auth_table)
                item = db.execute(stmt).fetchone()
                authconfigdefault = item._mapping if item else None

                stmt = select(origin_table.c.link).where(origin_table.c.deleted_at.is_(None))
                result = db.execute(stmt).scalars().all()
                allow_origins = result if result else ["*"]


class ConfigAuth(BaseModel):
    SSO_LOGIN_URL: str = authconfigdefault["sso_login_url"]
    SSO_TOKEN_URL: str = authconfigdefault["sso_token_url"]
    SSO_CLIENT_ID: str = authconfigdefault["sso_client_id"]
    JWT_SECRET_KEY: str = authconfigdefault["jwt_scret_key"]
    JWT_ALGORITHM: str = authconfigdefault["jwt_algorithm"]
    COOKIES_PREFIX: str = authconfigdefault["cookies_prefix"]
    COOKIES_HTTPS: bool = authconfigdefault["cookies_https"]
    COOKIES_EXPIRED: int = authconfigdefault["cookies_exp"]
    REFRESH_EXPIRED: int = authconfigdefault["refresh_exp"]
    TIMEOUT_EXPIRED: int = authconfigdefault["timeout_exp"]
    CLIENT_KEY: str = authconfigdefault["cookies_prefix"] + "client"
    COOKIES_KEY: str = authconfigdefault["cookies_prefix"] + "token"
    REFRESH_KEY: str = authconfigdefault["cookies_prefix"] + "refresh"
    REGISTER_ACCOUNT: bool = authconfigdefault["register_account"]
    LOGIN_BY_OTP: bool = authconfigdefault["login_by_otp"]


class Config(BaseModel):
    APP_NAME: str = configdefault["app_name"]
    APP_DESCRIPTION: str = configdefault["app_desc"]
    APP_VERSION: str = version_name
    ENV: str = configdefault["environment"]
    DEBUG: bool = configdefault["debug"]
    APP_HOST: str = configdefault["app_host"]
    APP_PORT: int = configdefault["app_port"]
    HOST_URL: int = configdefault["host_url"]
    REPOSITORY: Dict[str, RepositoryModel] = repository
    ALLOW_ORIGINS: list[str] = allow_origins


config: Config = Config()
config_auth: ConfigAuth = ConfigAuth()
