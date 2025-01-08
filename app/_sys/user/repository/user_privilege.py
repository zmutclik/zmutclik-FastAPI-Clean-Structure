from typing import Optional, List, Union
from datetime import datetime

from abc import ABCMeta, abstractmethod
from sqlalchemy import or_, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from core.db import session
from core.exceptions import DatabaseSavingException, DatabaseUpdatingException, DatabaseDeletingException

from app._sys.user.domain import UserPrivilege


class UserPrivilegeRepo:
    __metaclass__ = ABCMeta

    @abstractmethod
    async def get_by_id(self, user_privilege_id: int) -> Optional[UserPrivilege]:
        pass

    @abstractmethod
    async def get(self, user_id: int, privilege_id: int) -> Optional[UserPrivilege]:
        pass

    @abstractmethod
    async def get_by_user(self, user_id: int) -> list[UserPrivilege]:
        pass

    @abstractmethod
    async def get_list_by_user(self, user_id: int) -> list[str]:
        pass

    @abstractmethod
    async def save(self, user_privilege: UserPrivilege) -> UserPrivilege:
        pass

    @abstractmethod
    async def delete(self, user_privilege: UserPrivilege) -> None:
        pass

    @abstractmethod
    async def delete_in_user(self, user_id: int) -> None:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass


class UserPrivilegeSQLRepo(UserPrivilegeRepo):
    async def get_by_id(self, user_privilege_id: int) -> Optional[UserPrivilege]:
        return await session.get(UserPrivilege, user_privilege_id)

    async def get(self, user_id: int, privilege_id: int) -> Optional[UserPrivilege]:
        result = await session.execute(
            select(UserPrivilege).where(
                or_(
                    UserPrivilege.user_id == user_id,
                    UserPrivilege.privilege_id == privilege_id,
                )
            )
        )
        return result.scalars().first()

    async def get_by_user(self, user_id: int) -> list[UserPrivilege]:
        result = await session.execute(
            select(UserPrivilege).where(
                or_(
                    UserPrivilege.user_id == user_id,
                )
            )
        )
        return result.scalars().all()

    async def get_list_by_user(self, user_id: int) -> list[int]:
        privileges = []
        for item in await self.get_by_user(user_id):
            privileges.append(item.privilege_id)
        return privileges

    async def save(self, user_privilege: UserPrivilege) -> UserPrivilege:
        try:
            session.add(user_privilege)
            await session.commit()
            await session.refresh(user_privilege)
            return user_privilege
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseSavingException(f"Error saving user: {str(e)}")

    async def delete(self, user_privilege: UserPrivilege) -> None:
        try:
            await session.delete(user_privilege)
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseDeletingException(f"Error deleting user: {str(e)}")

    async def delete_in_user(self, user_id: int) -> None:
        try:
            await session.execute(delete(UserPrivilege).where(UserPrivilege.user_id == user_id))
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseDeletingException(f"Error deleting user: {str(e)}")

    async def commit(self) -> None:
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseDeletingException(f"Error deleting user: {str(e)}")
