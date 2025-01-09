from typing import Optional, List, Union
from datetime import datetime

from abc import ABCMeta, abstractmethod
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app._sys.privilege.domain import Privilege
from core.db import session
from core.exceptions import DatabaseSavingException, DatabaseUpdatingException, DatabaseDeletingException


class PrivilegeRepo:

    __metaclass__ = ABCMeta

    @abstractmethod
    async def get_privilege(self, privilege: str) -> Optional[Privilege]:
        pass

    @abstractmethod
    async def get_privileges(self) -> list[Privilege]:
        pass

    @abstractmethod
    async def get_privilege_by_id(self, privilege_id: int) -> Optional[Privilege]:
        pass

    @abstractmethod
    async def save_privilege(self, privilege: Privilege) -> Privilege:
        pass

    @abstractmethod
    async def update_privilege(self, privilege: Privilege, **kwargs) -> Privilege:
        pass

    @abstractmethod
    async def delete_privilege(self, privilege: Privilege, deleted_user: str) -> None:
        pass


class PrivilegeSQLRepo(PrivilegeRepo):
    async def get_privilege(self, privilege: str) -> Optional[Privilege]:
        result = await session.execute(select(Privilege).where(Privilege.privilege == privilege, Privilege.deleted_at == None))
        return result.scalars().first()

    async def get_privileges(self) -> list[Privilege]:
        result = await session.execute(select(Privilege).where(Privilege.deleted_at == None).order_by(Privilege.privilege))
        return result.scalars().all()

    async def get_privilege_by_id(self, privilege_id: int) -> Optional[Privilege]:
        return await session.get(Privilege, privilege_id)

    async def save_privilege(self, privilege: Privilege) -> Privilege:
        try:
            await session.add(privilege)
            await session.commit()
            await session.refresh(privilege)
            return privilege
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseSavingException(f"Error saving user: {str(e)}")

    async def update_privilege(self, privilege: Privilege, **kwargs) -> Privilege:
        try:
            for key, value in kwargs.items():
                if hasattr(privilege, key) and value is not None:
                    setattr(privilege, key, value)
            await session.commit()
            await session.refresh(privilege)
            return privilege
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseUpdatingException(f"Error updating user: {str(e)}")

    async def delete_privilege(self, privilege: Privilege, deleted_user: str) -> None:
        try:
            if not privilege.deleted_at:
                privilege.deleted_at = datetime.now()
                privilege.deleted_user = deleted_user
                await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseDeletingException(f"Error deleting user: {str(e)}")
