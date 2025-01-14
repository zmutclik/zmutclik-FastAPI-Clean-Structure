from typing import Optional, List, Union
from datetime import datetime

from abc import ABCMeta, abstractmethod
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app._sys.menutype.domain import MenuType
from core.db import session_menu as session
from core.exceptions import DatabaseSavingException, DatabaseUpdatingException, DatabaseDeletingException


class MenuTypeRepo:

    __metaclass__ = ABCMeta

    @abstractmethod
    async def get_menutype(self, menutype_id: int) -> Optional[MenuType]:
        pass

    @abstractmethod
    async def get_menutype_by(self, menutype: str) -> Optional[MenuType]:
        pass

    @abstractmethod
    async def get_menutypes(self) -> list[MenuType]:
        pass

    @abstractmethod
    async def save_menutype(self, menutype: MenuType) -> MenuType:
        pass

    @abstractmethod
    async def update_menutype(self, menutype: MenuType, **kwargs) -> MenuType:
        pass

    @abstractmethod
    async def delete_menutype(self, menutype: MenuType, deleted_user: str) -> None:
        pass


class MenuTypeSQLRepo(MenuTypeRepo):
    async def get_menutype(self, menutype_id: int) -> Optional[MenuType]:
        return await session.get(MenuType, menutype_id)

    async def get_menutype_by(self, menutype: str) -> Optional[MenuType]:
        result = await session.execute(select(MenuType).where(MenuType.menutype == menutype, MenuType.deleted_at == None))
        return result.scalars().first()

    async def get_menutypes(self) -> list[MenuType]:
        result = await session.execute(select(MenuType).where(MenuType.deleted_at == None).order_by(MenuType.menutype))
        return result.scalars().all()

    async def save_menutype(self, menutype: MenuType) -> MenuType:
        try:
            await session.add(menutype)
            await session.commit()
            await session.refresh(menutype)
            return menutype
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseSavingException(f"Error saving menutype: {str(e)}")

    async def update_menutype(self, menutype: MenuType, **kwargs) -> MenuType:
        try:
            for key, value in kwargs.items():
                if hasattr(menutype, key) and value is not None:
                    setattr(menutype, key, value)
            await session.commit()
            await session.refresh(menutype)
            return menutype
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseUpdatingException(f"Error updating menutype: {str(e)}")

    async def delete_menutype(self, menutype: MenuType, deleted_user: str) -> None:
        try:
            if not menutype.deleted_at:
                menutype.deleted_at = datetime.now()
                menutype.deleted_user = deleted_user
                await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseDeletingException(f"Error deleting menutype: {str(e)}")
