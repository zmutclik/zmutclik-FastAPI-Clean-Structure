from typing import Optional, List, Union
from datetime import datetime

from abc import ABCMeta, abstractmethod
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from core.app.system.coresystem.domain import CoreSYSTEM
from core.db import session_core as session
from core.exceptions import DatabaseSavingException, DatabaseUpdatingException, DatabaseDeletingException


class CoreSYSTEMRepo:

    __metaclass__ = ABCMeta

    @abstractmethod
    async def get(self) -> Optional[CoreSYSTEM]:
        pass

    @abstractmethod
    async def update(self, coresystem: CoreSYSTEM, **kwargs) -> CoreSYSTEM:
        pass


class CoreSYSTEMSQLRepo(CoreSYSTEMRepo):
    async def get(self) -> Optional[CoreSYSTEM]:
        result = await session.execute(select(CoreSYSTEM))
        return result.scalars().first()

    async def update(self, coresystem: CoreSYSTEM, **kwargs) -> CoreSYSTEM:
        try:
            for key, value in kwargs.items():
                if hasattr(coresystem, key) and value is not None:
                    setattr(coresystem, key, value)
            await session.commit()
            await session.refresh(coresystem)
            return coresystem
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseUpdatingException(f"Error updating coresystem: {str(e)}")
