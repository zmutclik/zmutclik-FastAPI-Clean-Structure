import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from contextvars import ContextVar, Token
from typing import Union
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_scoped_session,
)
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

from core import config
from .base import BaseCore as Base
from app._sys.changelog.domain import ChangeLog
from app._sys.crossorigin.domain import CrossOrigin
from app._sys.menu.domain import Menu
from app._sys.menutype.domain import MenuType
from app._sys.privilege.domain import Privilege
from app._sys.scope.domain import Scope
from app._sys.sysrepo.domain import SysRepo
from app._sys.user.domain import User, UserPrivilege, UserScope

session_context: ContextVar[str] = ContextVar("session_context_core")


def get_session_id() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


# try:
#     dbcore_engine = create_engine(config.DBCORE_URL.replace("aiomysql", "pymysql"))
#     with dbcore_engine.begin() as connection:
#         if not dbcore_engine.dialect.has_table(table_name="sys_cross_origin", connection=connection):
#             Base.metadata.create_all(bind=dbcore_engine)
# except OperationalError as err:
#     if "1045" in err.args[0]:
#         print("DATABASE CORE : Access Denied")
#     elif "2003" in err.args[0]:
#         print("DATABASE CORE : Connection Refused")
#     else:
#         raise


DB_FILE = ".db/system/core.db"
DB_ENGINE = "sqlite+aiosqlite:///" + DB_FILE
dbcore_engine = create_engine(DB_ENGINE.replace("+aiosqlite", ""))
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        f.write("")

if os.path.exists(DB_FILE):
    file_stats = os.stat(DB_FILE)
    if file_stats.st_size == 0:
        Base.metadata.create_all(bind=dbcore_engine)
        with dbcore_engine.begin() as connection:
            with Session(bind=connection) as db:
                db.add(
                    User(
                        **{
                            "username": "admin",
                            "email": "admin@test.id",
                            "nohp": "62812345678",
                            "full_name": "Admin SeMuT",
                            "hashed_password": "$2b$12$ofIPPqnjPf54SzEvctr3DOzNqyjZQqDaA3GraVDvBobo/UfjtGqQm",
                            "created_user": "init_app",
                        }
                    )
                )
                db.add(Scope(**{"scope": "read", "desc": "", "created_user": "init_app"}))
                db.add(Scope(**{"scope": "write", "desc": "", "created_user": "init_app"}))
                db.add(Scope(**{"scope": "delete", "desc": "", "created_user": "init_app"}))
                db.add(Privilege(**{"privilege": "system", "desc": "Privilage Khusus Administrator Core System", "created_user": "init_app"}))
                db.add(Privilege(**{"privilege": "admin", "desc": "Privilage Khusus Administrator Applikasi", "created_user": "init_app"}))
                db.add(Privilege(**{"privilege": "user", "desc": "Privilage Standart Users", "created_user": "init_app"}))
                db.commit()
                db.add(UserPrivilege(**{"id": 1, "user_id": 1, "privilege_id": 1}))
                db.add(UserPrivilege(**{"id": 2, "user_id": 1, "privilege_id": 2}))
                db.add(UserPrivilege(**{"id": 3, "user_id": 1, "privilege_id": 3}))
                db.add(UserScope(**{"id": 1, "user_id": 1, "scope_id": 1}))
                db.add(UserScope(**{"id": 2, "user_id": 1, "scope_id": 2}))
                db.add(UserScope(**{"id": 3, "user_id": 1, "scope_id": 3}))
                db.commit()


async_engine = create_async_engine(DB_ENGINE)  # , echo=True)
async_session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

session_core: Union[AsyncSession, async_scoped_session] = async_scoped_session(
    session_factory=async_session,
    scopefunc=get_session_id,
)
