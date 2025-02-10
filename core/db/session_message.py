import os
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextvars import ContextVar, Token
from typing import Union
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session

from sqlalchemy import create_engine

from .base import BaseMessage as Base

from core.app.logs.domain import Logs

session_context: ContextVar[str] = ContextVar("session_context_messages")


def get_session_id() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


def async_engine(tahunbulan: datetime = None):
    if tahunbulan is None:
        tahunbulan = datetime.now()

    DB_FILE = ".db/logs/message_{}.db".format(tahunbulan.strftime("%Y"))
    DB_ENGINE = "sqlite+aiosqlite:///" + DB_FILE
    db_engine = create_engine(DB_ENGINE.replace("+aiosqlite", ""))

    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            f.write("")

    if os.path.exists(DB_FILE):
        file_stats = os.stat(DB_FILE)
        if file_stats.st_size == 0:
            Base.metadata.create_all(bind=db_engine)

    return create_async_engine(DB_ENGINE)


async_session = sessionmaker(bind=async_engine(), class_=AsyncSession, expire_on_commit=False)
session_message: Union[AsyncSession, async_scoped_session] = async_scoped_session(
    session_factory=async_session,
    scopefunc=get_session_id,
)
