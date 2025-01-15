from typing import Optional, List, Union
from datetime import datetime

from abc import ABCMeta, abstractmethod
from sqlalchemy import or_, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from core.db import session_auth as session
from core.exceptions import DatabaseSavingException, DatabaseUpdatingException, DatabaseDeletingException

from ..domain import PrivilegeMenus


class PrivilegeMenusRepo:
    __metaclass__ = ABCMeta

    @abstractmethod
    async def get_privilege_menu(self, privilege_menu_id: int) -> Optional[PrivilegeMenus]:
        pass

    @abstractmethod
    async def get_privilege_menu_by(self, privilege_id: int, menu_id: int) -> Optional[PrivilegeMenus]:
        pass

    @abstractmethod
    async def get_privilege_menus(self, privilege_id: int) -> list[PrivilegeMenus]:
        pass

    @abstractmethod
    async def save_privilege_menu(self, privilege_menu: PrivilegeMenus) -> PrivilegeMenus:
        pass

    @abstractmethod
    async def delete_privilege_menu(self, privilege_menu: PrivilegeMenus) -> None:
        pass

    @abstractmethod
    async def delete_privilege_menus(self, privilege_id: int, menutype_id: int) -> None:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass


class PrivilegeMenusSQLRepo(PrivilegeMenusRepo):
    async def get_privilege_menu(self, privilege_menu_id: int) -> Optional[PrivilegeMenus]:
        return await session.get(PrivilegeMenus, privilege_menu_id)

    async def get_privilege_menu_by(self, privilege_id: int, menu_id: int) -> Optional[PrivilegeMenus]:
        result = await session.execute(
            select(PrivilegeMenus).where(
                or_(
                    PrivilegeMenus.menu_id == menu_id,
                    PrivilegeMenus.privilege_id == privilege_id,
                )
            )
        )
        return result.scalars().first()

    async def get_privilege_menus(self, privilege_id: int) -> list[PrivilegeMenus]:
        result = await session.execute(select(PrivilegeMenus).where(PrivilegeMenus.privilege_id == privilege_id))
        return result.scalars().all()

    async def save_privilege_menu(self, privilege_menu: PrivilegeMenus) -> PrivilegeMenus:
        try:
            session.add(privilege_menu)
            await session.commit()
            await session.refresh(privilege_menu)
            return privilege_menu
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseSavingException(f"Error saving privilege menu: {str(e)}")

    async def delete_privilege_menu(self, privilege_menu: PrivilegeMenus) -> None:
        try:
            await session.delete(privilege_menu)
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseDeletingException(f"Error deleting privilege menu: {str(e)}")

    async def delete_privilege_menus(self, privilege_id: int, menutype_id: int) -> None:
        try:
            await session.execute(
                delete(PrivilegeMenus).where(
                    PrivilegeMenus.privilege_id == privilege_id,
                    PrivilegeMenus.menutype_id == menutype_id,
                )
            )
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseDeletingException(f"Error deleting privilege menu: {str(e)}")

    async def commit(self) -> None:
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseDeletingException(f"Error commit: {str(e)}")
