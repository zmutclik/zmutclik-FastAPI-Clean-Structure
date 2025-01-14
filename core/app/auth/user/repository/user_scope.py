from typing import Optional, List, Union
from datetime import datetime

from abc import ABCMeta, abstractmethod
from sqlalchemy import or_, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from core.db import session_auth as session
from core.exceptions import DatabaseSavingException, DatabaseUpdatingException, DatabaseDeletingException

from ..domain import UserScope


class UserScopeRepo:
    __metaclass__ = ABCMeta

    @abstractmethod
    async def get_by_id(self, user_scope_id: int) -> Optional[UserScope]:
        pass

    @abstractmethod
    async def get(self, user_id: int, scope_id: int) -> Optional[UserScope]:
        pass

    @abstractmethod
    async def get_by_user(self, user_id: int) -> list[UserScope]:
        pass

    @abstractmethod
    async def get_list_by_user(self, user_id: int) -> list[str]:
        pass

    @abstractmethod
    async def save(self, user_scope: UserScope) -> UserScope:
        pass

    @abstractmethod
    async def delete(self, user_scope: UserScope) -> None:
        pass

    @abstractmethod
    async def delete_in_user(self, user_id: int) -> None:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass


class UserScopeSQLRepo(UserScopeRepo):
    async def get_by_id(self, user_scope_id: int) -> Optional[UserScope]:
        return await session.get(UserScope, user_scope_id)

    async def get(self, user_id: int, scope_id: int) -> Optional[UserScope]:
        result = await session.execute(
            select(UserScope).where(
                or_(
                    UserScope.user_id == user_id,
                    UserScope.scope_id == scope_id,
                )
            )
        )
        return result.scalars().first()

    async def get_by_user(self, user_id: int) -> list[UserScope]:
        result = await session.execute(
            select(UserScope).where(
                or_(
                    UserScope.user_id == user_id,
                )
            )
        )
        return result.scalars().all()

    async def get_list_by_user(self, user_id: int) -> list[int]:
        scopes = []
        for item in await self.get_by_user(user_id):
            scopes.append(item.id)
        return scopes

    async def save(self, user_scope: UserScope) -> UserScope:
        try:
            session.add(user_scope)
            await session.commit()
            await session.refresh(user_scope)
            return user_scope
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseSavingException(f"Error saving user: {str(e)}")

    async def delete(self, user_scope: UserScope) -> None:
        try:
            await session.delete(user_scope)
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseDeletingException(f"Error deleting user: {str(e)}")

    async def delete_in_user(self, user_id: int) -> None:
        try:
            await session.execute(delete(UserScope).where(UserScope.user_id == user_id))
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseDeletingException(f"Error deleting user: {str(e)}")

    async def commit(self) -> None:
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseDeletingException(f"Error deleting user: {str(e)}")
