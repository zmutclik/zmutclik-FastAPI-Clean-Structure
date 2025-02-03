from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextvars import ContextVar, Token
from typing import Union
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session

from core.config import DBSECURITY_ENGINE

session_context: ContextVar[str] = ContextVar("session_context_security")


def get_session_id() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


async_engine = create_async_engine(DBSECURITY_ENGINE)  # , echo=True)
async_session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

session_security: Union[AsyncSession, async_scoped_session] = async_scoped_session(
    session_factory=async_session,
    scopefunc=get_session_id,
)
