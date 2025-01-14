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
from .base import BaseMenu as Base
from core.app.menu.menu.domain import Menu
from core.app.menu.menutype.domain import MenuType

session_context: ContextVar[str] = ContextVar("session_context_menu")


def get_session_id() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


DB_FILE = ".db/system/menu.db"
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
                pass


async_engine = create_async_engine(DB_ENGINE)  # , echo=True)
async_session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

session_menu: Union[AsyncSession, async_scoped_session] = async_scoped_session(
    session_factory=async_session,
    scopefunc=get_session_id,
)
