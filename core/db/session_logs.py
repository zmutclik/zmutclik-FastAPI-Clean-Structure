from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextvars import ContextVar, Token
from typing import Union
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

from core import config
from .base import BaseLogs as Base

from app._sys.logs.domain import Logs

session_context: ContextVar[str] = ContextVar("session_context_logs")


def get_session_id() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


try:
    dblogs_engine = create_engine(config.DBLOGS_URL.replace("aiomysql", "pymysql"))
    with dblogs_engine.begin() as connection:
        if not dblogs_engine.dialect.has_table(table_name="logs", connection=connection):
            Base.metadata.create_all(bind=dblogs_engine)
except OperationalError as err:
    if "1045" in err.args[0]:
        print("DATABASE LOGS : Access Denied")
    elif "2003" in err.args[0]:
        print("DATABASE LOGS : Connection Refused")
    else:
        raise

async_engine = create_async_engine(config.DBLOGS_URL)  # , echo=True)
async_session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)
session_logs: Union[AsyncSession, async_scoped_session] = async_scoped_session(
    session_factory=async_session,
    scopefunc=get_session_id,
)
