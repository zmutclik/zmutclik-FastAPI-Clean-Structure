from typing import Optional, List, Union
from datetime import datetime

from abc import ABCMeta, abstractmethod
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from ..domain import ChangeLog
from core.db import session_core as session
from core.exceptions import DatabaseSavingException, DatabaseUpdatingException, DatabaseDeletingException


class ChangeLogRepo:

    __metaclass__ = ABCMeta

    @abstractmethod
    async def get_changelog(self, changelog_id: int) -> Optional[ChangeLog]:
        pass

    @abstractmethod
    async def get_changelog_by(self, version_name: str) -> Optional[ChangeLog]:
        pass

    @abstractmethod
    async def get_last_changelog(self) -> Optional[ChangeLog]:
        pass

    @abstractmethod
    async def save_changelog(self, changelog: ChangeLog) -> ChangeLog:
        pass

    @abstractmethod
    async def update_changelog(self, changelog: ChangeLog, **kwargs) -> ChangeLog:
        pass

    @abstractmethod
    async def delete_changelog(self, changelog: ChangeLog, deleted_user: str) -> None:
        pass


class ChangeLogRepoSQLRepo(ChangeLogRepo):
    async def get_changelog(self, changelog_id: int) -> Optional[ChangeLog]:
        return await session.get(ChangeLog, changelog_id)

    async def get_changelog_by(self, version_name: str) -> Optional[ChangeLog]:
        result = await session.execute(select(ChangeLog).where(ChangeLog.version_name == version_name))
        return result.scalars().first()

    async def get_last_changelog(self) -> Optional[ChangeLog]:
        result = await session.execute(select(ChangeLog).where(ChangeLog.deleted_at == None).order_by(ChangeLog.id.desc()))
        return result.scalars().first()

    async def save_changelog(self, changelog: ChangeLog) -> ChangeLog:
        try:
            session.add(changelog)
            await session.commit()
            await session.refresh(changelog)
            return changelog
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseSavingException(f"Error saving user: {str(e)}")

    async def update_changelog(self, changelog: ChangeLog, **kwargs) -> ChangeLog:
        try:
            for key, value in kwargs.items():
                if hasattr(changelog, key) and value is not None:
                    setattr(changelog, key, value)
            await session.commit()
            await session.refresh(changelog)
            return changelog
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseUpdatingException(f"Error updating user: {str(e)}")

    async def delete_changelog(self, changelog: ChangeLog, deleted_user: str) -> None:
        try:
            if not changelog.deleted_at:
                changelog.deleted_at = datetime.now()
                changelog.deleted_user = deleted_user
                await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseDeletingException(f"Error deleting user: {str(e)}")
