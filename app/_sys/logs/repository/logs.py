from typing import Optional, List, Union
from datetime import datetime

from abc import ABCMeta, abstractmethod
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app._sys.logs.domain import Logs
from core.db import session
from core.exceptions import DatabaseSavingException, DatabaseUpdatingException, DatabaseDeletingException


class LogsRepo:

    __metaclass__ = ABCMeta

    @abstractmethod
    async def get_by_id(self, logs_id: int) -> Optional[Logs]:
        pass

    @abstractmethod
    async def save(self, logs: Logs) -> Logs:
        pass


class LogsSQLRepo(LogsRepo):
    async def get_by_id(self, logs_id: int) -> Optional[Logs]:
        return await session.get(Logs, logs_id)

    async def save(self, logs: Logs) -> Logs:
        try:
            await session.add(logs)
            await session.commit()
            await session.refresh(logs)
            return logs
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseSavingException(f"Error saving logs: {str(e)}")
