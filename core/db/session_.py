import sys
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextvars import ContextVar, Token
from typing import Union
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session
from sqlalchemy.exc import ArgumentError

from core.config import config

session_context: ContextVar[str] = ContextVar("session_context_app")


def get_session_id() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


try:
    data_dbapps = config.REPOSITORY["DBAPPS_URL_DEFAULT"]
    async_engine = create_async_engine(data_dbapps.datalink)  # , echo=True)
except ArgumentError as err:
    print(f"Error: APPLIKASI GAGAL START KARENA INISIASI CORE DATABASE -> RESTART APPLIKASI")
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
