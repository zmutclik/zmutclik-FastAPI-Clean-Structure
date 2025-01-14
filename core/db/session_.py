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
from sqlalchemy.exc import OperationalError, ArgumentError

from core import config
from .base import Base

DBAPPS_URL: str = config.DBAPPS_URL
session_context: ContextVar[str] = ContextVar("session_context_app")


def get_session_id() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


try:
    dbapps_engine = create_engine(DBAPPS_URL.replace("aiomysql", "pymysql"))
    with dbapps_engine.begin() as connection:
        if not dbapps_engine.dialect.has_table(table_name="app", connection=connection):
            Base.metadata.create_all(bind=dbapps_engine)
except ArgumentError as err:
    print(err)

except OperationalError as err:
    if "1045" in err.args[0]:
        print("DATABASE APPS : Access Denied")
    elif "1698" in err.args[0]:
        print("DATABASE APPS : Access Denied")
    elif "2003" in err.args[0]:
        print("DATABASE APPS : Connection Refused")
    elif "Could not parse SQLAlchemy URL from string" in err.args[0]:
        print("DATABASE APPS : URL Enggine ERROR")
    else:
        raise

try:
    async_engine = create_async_engine(DBAPPS_URL)  # , echo=True)
except ArgumentError as err:
    print(f"Error: APPLIKASI GAGAL START KARENA INISIASI CORE DATABASE -> RESTART APPLIKASI")
    import sys
    sys.exit(1)
    
async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

session: Union[AsyncSession, async_scoped_session] = async_scoped_session(
    session_factory=async_session,
    scopefunc=get_session_id,
)
