from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from contextvars import ContextVar, Token
import asyncio
from typing import Generator, AsyncGenerator, Union
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_scoped_session,
)

from core import config
from .base import Base

session_context: ContextVar[str] = ContextVar("session_context")


def get_session_id() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)

async_engine = create_async_engine(config.DB_URL, echo=True)
async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
session: Union[AsyncSession, async_scoped_session] = async_scoped_session(
    session_factory=async_session,
    scopefunc=get_session_id,
)
# class DBSessionWrapper:
#     def __init__(self, session_factory):
#         self._session_factory = session_factory

#     def __await__(self):
#         return self._get_session().__await__()

#     @asynccontextmanager
#     async def _generate_session(self):
#         async with self._session_factory() as session:
#             try:
#                 yield session
#             finally:
#                 await session.close()

#     async def _get_session(self):
#         async with self._generate_session() as session:
#             return session

#     async def __call__(self):
#         return await self._get_session()


# session: Generator[AsyncSession, None, None] = DBSessionWrapper(async_session)

