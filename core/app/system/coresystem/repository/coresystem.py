from typing import Optional, List, Union
from datetime import datetime

from abc import ABCMeta, abstractmethod
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from core.app.system.coresystem.domain import CoreSYSTEM
from core.db import session
from core.exceptions import DatabaseSavingException, DatabaseUpdatingException, DatabaseDeletingException


class CoreSYSTEMRepo:

    __metaclass__ = ABCMeta

    @abstractmethod
    async def get(self, coresystem: str) -> Optional[CoreSYSTEM]:
        pass

    @abstractmethod
    async def get_by_id(self, coresystem_id: int) -> Optional[CoreSYSTEM]:
        pass

    @abstractmethod
    async def save(self, coresystem: CoreSYSTEM) -> CoreSYSTEM:
        pass

    @abstractmethod
    async def update(self, coresystem: CoreSYSTEM, **kwargs) -> CoreSYSTEM:
        pass

    @abstractmethod
    async def delete(self, coresystem: CoreSYSTEM, deleted_user: str) -> None:
        pass


class CoreSYSTEMSQLRepo(CoreSYSTEMRepo):
    async def get(self, coresystem: str) -> Optional[CoreSYSTEM]:
        result = await session.execute(select(CoreSYSTEM).where(CoreSYSTEM.coresystem == coresystem))
        return result.scalars().first()

    async def get_by_id(self, coresystem_id: int) -> Optional[CoreSYSTEM]:
        return await session.get(CoreSYSTEM, coresystem_id)

    async def save(self, coresystem: CoreSYSTEM) -> CoreSYSTEM:
        try:
            await session.add(coresystem)
            await session.commit()
            await session.refresh(coresystem)
            return coresystem
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseSavingException(f"Error saving coresystem: {str(e)}")

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

    async def delete(self, coresystem: CoreSYSTEM, deleted_user: str) -> None:
        try:
            if not coresystem.deleted_at:
                coresystem.deleted_at = datetime.now()
                coresystem.deleted_user = deleted_user
                await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseDeletingException(f"Error deleting coresystem: {str(e)}")
