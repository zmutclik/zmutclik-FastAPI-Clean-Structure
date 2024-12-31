from typing import Optional, List, Union
from datetime import datetime

from abc import ABCMeta, abstractmethod
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.VARNAME.domain import CLASSNAME
from core.db import session
from core.exceptions import DatabaseSavingException, DatabaseUpdatingException, DatabaseDeletingException


class CLASSNAMERepo:

    __metaclass__ = ABCMeta

    @abstractmethod
    async def get(self, VARNAME: str) -> Optional[CLASSNAME]:
        pass

    @abstractmethod
    async def get_by_id(self, VARNAME_id: int) -> Optional[CLASSNAME]:
        pass

    @abstractmethod
    async def save(self, VARNAME: CLASSNAME) -> CLASSNAME:
        pass

    @abstractmethod
    async def update(self, VARNAME: CLASSNAME, **kwargs) -> CLASSNAME:
        pass

    @abstractmethod
    async def delete(self, VARNAME: CLASSNAME, deleted_user: str) -> None:
        pass


class CLASSNAMESQLRepo(CLASSNAMERepo):
    async def get(self, VARNAME: str) -> Optional[CLASSNAME]:
        result = await session.execute(select(CLASSNAME).where(CLASSNAME.VARNAME == VARNAME))
        return result.scalars().first()

    async def get_by_id(self, VARNAME_id: int) -> Optional[CLASSNAME]:
        return await session.get(CLASSNAME, VARNAME_id)

    async def save(self, VARNAME: CLASSNAME) -> CLASSNAME:
        try:
            await session.add(VARNAME)
            await session.commit()
            await session.refresh(VARNAME)
            return VARNAME
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseSavingException(f"Error saving VARNAME: {str(e)}")

    async def update(self, VARNAME: CLASSNAME, **kwargs) -> CLASSNAME:
        try:
            for key, value in kwargs.items():
                if hasattr(VARNAME, key) and value is not None:
                    setattr(VARNAME, key, value)
            await session.commit()
            await session.refresh(VARNAME)
            return VARNAME
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseUpdatingException(f"Error updating VARNAME: {str(e)}")

    async def delete(self, VARNAME: CLASSNAME, deleted_user: str) -> None:
        try:
            if not VARNAME.deleted_at:
                VARNAME.deleted_at = datetime.now()
                VARNAME.deleted_user = deleted_user
                await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseDeletingException(f"Error deleting VARNAME: {str(e)}")
