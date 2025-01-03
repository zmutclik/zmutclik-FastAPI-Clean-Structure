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
from .base import Base

session_context: ContextVar[str] = ContextVar("session_context_app")


def get_session_id() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


try:
    dbapps_engine = create_engine(config.DBAPPS_URL.replace("aiomysql", "pymysql"))
    with dbapps_engine.begin() as connection:
        if not dbapps_engine.dialect.has_table(table_name="app", connection=connection):
            Base.metadata.create_all(bind=dbapps_engine)
except OperationalError as err:
    if "1045" in err.args[0]:
        print("DATABASE APPS : Access Denied")
    elif "2003" in err.args[0]:
        print("DATABASE APPS : Connection Refused")
    else:
        raise

async_engine = create_async_engine(config.DBAPPS_URL)  # , echo=True)
async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

session: Union[AsyncSession, async_scoped_session] = async_scoped_session(
    session_factory=async_session,
    scopefunc=get_session_id,
)
