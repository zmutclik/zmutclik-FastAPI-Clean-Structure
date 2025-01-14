from typing import Optional, List, Union
from datetime import datetime

from abc import ABCMeta, abstractmethod
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from ..domain import SysRepo
from core.db import session_core as session
from core.exceptions import DatabaseSavingException, DatabaseUpdatingException, DatabaseDeletingException


class SysRepoRepo:

    __metaclass__ = ABCMeta

    @abstractmethod
    async def get_sysrepo(self, sysrepo_id: int) -> Optional[SysRepo]:
        pass

    @abstractmethod
    async def get_sysrepo_by(self, allocation: str, name: str) -> Optional[SysRepo]:
        pass

    @abstractmethod
    async def get_sysrepo_active(self, allocation: str) -> Optional[SysRepo]:
        pass

    @abstractmethod
    async def save_sysrepo(self, sysrepo: SysRepo) -> SysRepo:
        pass

    @abstractmethod
    async def update_sysrepo(self, sysrepo: SysRepo, **kwargs) -> SysRepo:
        pass

    @abstractmethod
    async def delete_sysrepo(self, sysrepo: SysRepo, deleted_user: str) -> None:
        pass


class SysRepoSQLRepo(SysRepoRepo):
    async def get_sysrepo(self, sysrepo_id: int) -> Optional[SysRepo]:
        return await session.get(SysRepo, sysrepo_id)

    async def get_sysrepo_by(self, allocation: str, name: str) -> Optional[SysRepo]:
        result = await session.execute(
            select(SysRepo)
            .where(
                SysRepo.deleted_at == None,
                SysRepo.allocation == allocation,
                SysRepo.name == name,
                SysRepo.is_active == True,
            )
            .order_by(SysRepo.id.desc())
        )
        return result.scalars().first()

    async def get_sysrepo_active(self, allocation: str) -> Optional[SysRepo]:
        result = await session.execute(
            select(SysRepo)
            .where(
                SysRepo.deleted_at == None,
                SysRepo.allocation == allocation,
                SysRepo.is_active == True,
            )
            .order_by(SysRepo.id.desc())
        )
        return result.scalars().first()

    async def save_sysrepo(self, sysrepo: SysRepo) -> SysRepo:
        try:
            await session.add(sysrepo)
            await session.commit()
            await session.refresh(sysrepo)
            return sysrepo
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseSavingException(f"Error saving user: {str(e)}")

    async def update_sysrepo(self, sysrepo: SysRepo, **kwargs) -> SysRepo:
        try:
            for key, value in kwargs.items():
                if hasattr(sysrepo, key) and value is not None:
                    setattr(sysrepo, key, value)
            await session.commit()
            await session.refresh(sysrepo)
            return sysrepo
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseUpdatingException(f"Error updating user: {str(e)}")

    async def delete_sysrepo(self, sysrepo: SysRepo, deleted_user: str) -> None:
        try:
            if not sysrepo.deleted_at:
                sysrepo.deleted_at = datetime.now()
                sysrepo.deleted_user = deleted_user
                await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseDeletingException(f"Error deleting user: {str(e)}")
