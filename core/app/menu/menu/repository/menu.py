from typing import Optional, List, Union
from datetime import datetime

from abc import ABCMeta, abstractmethod
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from ..domain import Menu
from core.db import session_menu as session
from core.exceptions import DatabaseSavingException, DatabaseUpdatingException, DatabaseDeletingException


class MenuRepo:

    __metaclass__ = ABCMeta

    @abstractmethod
    async def get_menu(self, menu_id: int) -> Optional[Menu]:
        pass

    @abstractmethod
    async def get_menu_by(self, menutype_id: int) -> list[Menu]:
        pass

    @abstractmethod
    async def save_menu(self, menu: Menu) -> Menu:
        pass

    @abstractmethod
    async def update_menu(self, menu: Menu, **kwargs) -> Menu:
        pass

    @abstractmethod
    async def delete_menu(self, menu: Menu, deleted_user: str) -> None:
        pass


class MenuSQLRepo(MenuRepo):
    async def get_menu(self, menu_id: int) -> Optional[Menu]:
        return await session.get(Menu, menu_id)

    async def get__menu_by(self, menutype_id: int) -> list[Menu]:
        result = await session.execute(
            select(Menu)
            .where(
                Menu.menutype_id == menutype_id,
                Menu.deleted_at == None,
            )
            .order_by(Menu.sort)
        )
        return result.scalars().all()

    async def save_menu(self, menu: Menu) -> Menu:
        try:
            await session.add(menu)
            await session.commit()
            await session.refresh(menu)
            return menu
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseSavingException(f"Error saving menu: {str(e)}")

    async def update_menu(self, menu: Menu, **kwargs) -> Menu:
        try:
            for key, value in kwargs.items():
                if hasattr(menu, key) and value is not None:
                    setattr(menu, key, value)
            await session.commit()
            await session.refresh(menu)
            return menu
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseUpdatingException(f"Error updating menu: {str(e)}")

    async def delete_menu(self, menu: Menu, deleted_user: str) -> None:
        try:
            if not menu.deleted_at:
                menu.deleted_at = datetime.now()
                menu.deleted_user = deleted_user
                await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseDeletingException(f"Error deleting menu: {str(e)}")
