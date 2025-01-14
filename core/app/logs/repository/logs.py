from uuid import uuid4
from typing import Optional, List, Union
from datetime import datetime
import time
from abc import ABCMeta, abstractmethod
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from core.app.logs.domain import Logs, IpAddress, RouterName
from core.exceptions import DatabaseSavingException

from core.db.session_logs import async_engine


class LogsRepo:
    def __init__(self) -> None:
        pass

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
