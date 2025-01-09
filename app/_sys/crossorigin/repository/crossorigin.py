from typing import Optional, List, Union
from datetime import datetime

from abc import ABCMeta, abstractmethod
from fastapi import Depends
from sqlalchemy import or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app._sys.crossorigin.domain import CrossOrigin
from core.db import session_core as session
from core.exceptions import DatabaseSavingException, DatabaseUpdatingException, DatabaseDeletingException


class CrossOriginRepo:

    __metaclass__ = ABCMeta

    @abstractmethod
    async def get_sys(self) -> list:
        pass

    @abstractmethod
    async def get_crossorigin(self, crossorigin_id: int) -> Optional[CrossOrigin]:
        pass

    @abstractmethod
    async def get_crossorigin_by(self, link: str) -> Optional[CrossOrigin]:
        pass

    @abstractmethod
    async def save_crossorigin(self, crossorigin: CrossOrigin) -> CrossOrigin:
        pass

    @abstractmethod
    async def update_crossorigin(self, crossorigin: CrossOrigin, **kwargs) -> CrossOrigin:
        pass

    @abstractmethod
    async def delete_crossorigin(self, crossorigin: CrossOrigin, deleted_user: str) -> None:
        pass


class CrossOriginSQLRepo(CrossOriginRepo):
    async def get_sys(self):
        result = await session.execute(select(CrossOrigin))
        res = []
        for item in result.scalars().all():
            res.append(item)
        if res == []:
            res.append("*")
        return res

    async def get_crossorigin(self, crossorigin_id: int) -> Optional[CrossOrigin]:
        return await session.get(CrossOrigin, crossorigin_id)

    async def get_crossorigin_by(self, link: str) -> Optional[CrossOrigin]:
        result = await session.execute(select(CrossOrigin).where(CrossOrigin.link == link))
        return result.scalars().first()

    async def save_crossorigin(self, crossorigin: CrossOrigin) -> CrossOrigin:
        try:
            await session.add(crossorigin)
            await session.commit()
            await session.refresh(crossorigin)
            return crossorigin
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseSavingException(f"Error saving crossorigin: {str(e)}")

    async def update_crossorigin(self, crossorigin: CrossOrigin, **kwargs) -> CrossOrigin:
        try:
            for key, value in kwargs.items():
                if hasattr(crossorigin, key) and value is not None:
                    setattr(crossorigin, key, value)
            await session.commit()
            await session.refresh(crossorigin)
            return crossorigin
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseUpdatingException(f"Error updating crossorigin: {str(e)}")

    async def delete_crossorigin(self, crossorigin: CrossOrigin, deleted_user: str) -> None:
        try:
            if not crossorigin.deleted_at:
                crossorigin.deleted_at = datetime.now()
                crossorigin.deleted_user = deleted_user
                await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseDeletingException(f"Error deleting crossorigin: {str(e)}")
