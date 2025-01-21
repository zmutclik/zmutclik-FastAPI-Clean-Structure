from typing import Optional, List, Union
from datetime import datetime

from abc import ABCMeta, abstractmethod
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from ..domain import Scope
from core.db import session_auth as session
from core.exceptions import DatabaseSavingException, DatabaseUpdatingException, DatabaseDeletingException


class ScopeRepo:

    __metaclass__ = ABCMeta

    @abstractmethod
    async def get_scope(self, scope_id: int) -> Optional[Scope]:
        pass

    @abstractmethod
    async def get_scope_by(self, scope: str) -> Optional[Scope]:
        pass

    @abstractmethod
    async def get_scopes(self) -> list[Scope]:
        pass

    @abstractmethod
    async def save_scope(self, scope: Scope) -> Scope:
        pass

    @abstractmethod
    async def update_scope(self, scope_data: Scope, **kwargs) -> Scope:
        pass

    @abstractmethod
    async def delete_scope(self, scope: Scope, deleted_user: str) -> None:
        pass


class ScopeSQLRepo(ScopeRepo):
    async def get_scope(self, scope_id: int) -> Optional[Scope]:
        return await session.get(Scope, scope_id)

    async def get_scope_by(self, scope: str) -> Optional[Scope]:
        result = await session.execute(select(Scope).where(Scope.scope == scope, Scope.deleted_at == None))
        return result.scalars().first()

    async def get_scopes(self) -> list[Scope]:
        result = await session.execute(select(Scope).where(Scope.deleted_at == None).order_by(Scope.id))
        return result.scalars().all()

    async def save_scope(self, scope: Scope) -> Scope:
        try:
            session.add(scope)
            await session.commit()
            await session.refresh(scope)
            return scope
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseSavingException(f"Error saving scope: {str(e)}")

    async def update_scope(self, scope_data: Scope, **kwargs) -> Scope:
        try:
            for key, value in kwargs.items():
                if hasattr(scope_data, key) and value is not None:
                    setattr(scope_data, key, value)
            await session.commit()
            await session.refresh(scope_data)
            return scope_data
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseUpdatingException(f"Error updating scope: {str(e)}")

    async def delete_scope(self, scope: Scope, deleted_user: str) -> None:
        try:
            if not scope.deleted_at:
                scope.deleted_at = datetime.now()
                scope.deleted_user = deleted_user
                await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseDeletingException(f"Error deleting scope: {str(e)}")
