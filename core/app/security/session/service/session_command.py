from typing import Union
import random
import string
from datetime import datetime

from ..domain import Session
from ..repository import SessionRepo
from core.db.session_security import async_engine
from sqlalchemy.ext.asyncio import AsyncSession


class SessionService:
    async def __generate_new_session(self, db: AsyncSession) -> str:
        newsession = "".join(random.choices(string.ascii_letters + string.digits, k=random.randint(3, 6)))
        if await SessionRepo().get_session_id(db, newsession) is not None:
            await self.__generate_new_session()
        return newsession

    async def create_session(self, client_id: str, user: str, session_end: datetime) -> None:
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                newsession = await self.__generate_new_session(db)
                data_create = Session.create(client_id=client_id, session_id=newsession, user=user, session_end=session_end)
                await SessionRepo().save_session(db, data_create)
                return newsession

    async def get_session_id(self, session_id: str):
        async with async_engine.begin() as connection:
            async with AsyncSession(bind=connection) as db:
                data_get = await SessionRepo().get_session_id(db, session_id)
                if data_get is not None:
                    await SessionRepo().session_update(db, data_get)
                return data_get
