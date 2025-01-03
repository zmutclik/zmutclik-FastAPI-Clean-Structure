from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
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
from app._sys.user.domain import User, UserPrivilege

session_context: ContextVar[str] = ContextVar("session_context_core")


def get_session_id() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


try:
    dbcore_engine = create_engine(config.DBCORE_URL.replace("aiomysql", "pymysql"))
    with dbcore_engine.begin() as connection:
        if not dbcore_engine.dialect.has_table(table_name="cross_origin", connection=connection):
            Base.metadata.create_all(bind=dbcore_engine)
except OperationalError as err:
    if "1045" in err.args[0]:
        print("DATABASE CORE : Access Denied")
    elif "2003" in err.args[0]:
        print("DATABASE CORE : Connection Refused")
    else:
        raise

async_engine = create_async_engine(config.DBCORE_URL)  # , echo=True)
async_session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

session_core: Union[AsyncSession, async_scoped_session] = async_scoped_session(
    session_factory=async_session,
    scopefunc=get_session_id,
)
