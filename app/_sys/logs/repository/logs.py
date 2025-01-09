from uuid import uuid4
from typing import Optional, List, Union
from datetime import datetime
import time
from abc import ABCMeta, abstractmethod
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app._sys.logs.domain import Logs, IpAddress, RouterName
from core.exceptions import DatabaseSavingException, DatabaseUpdatingException, DatabaseDeletingException

from sqlalchemy.orm import Session
from core.db.session_logs import set_session_context, reset_session_context, session_logs, async_session, async_engine


class LogsRepo:
    def __init__(self, tahunbulan: datetime = None) -> None:
        if tahunbulan is None:
            tahunbulan = datetime.now()
        pass

    async def get_by_id(self, logs_id: int) -> Optional[Logs]:
        return await self.db.get(Logs, logs_id)

    async def save(self, logs: Logs):
        async with async_engine().begin() as connection:
            async with AsyncSession(bind=connection) as db:
                try:
                    db.add(logs)
                    db.add(IpAddress(ipaddress=logs.ipaddress))
                    db.add(RouterName(routername=logs.router))
                    await db.commit()
                except SQLAlchemyError as e:
                    raise DatabaseSavingException(f"Error saving logs: {str(e)}")
