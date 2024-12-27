from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

from core import config


async_engine = create_async_engine(config.DB_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class DBSessionWrapper:
    def __init__(self, session_factory):
        self._session_factory = session_factory

    def __await__(self):
        return self._get_session().__await__()

    @asynccontextmanager
    async def _generate_session(self):
        async with self._session_factory() as session:
            try:
                yield session
            finally:
                await session.close()

    async def _get_session(self):
        async with self._generate_session() as session:
            return session

    async def __call__(self):
        return await self._get_session()


session: AsyncSession = DBSessionWrapper(AsyncSessionLocal)


# @asynccontextmanager
# async def get_db():
#     async with AsyncSessionLocal() as session:
#         try:
#             yield session
#         finally:
#             await session.close()
