from typing import Optional, List, Union
from abc import ABCMeta, abstractmethod
from sqlalchemy import or_, select, delete
from sqlalchemy.exc import SQLAlchemyError

from core.db import session_auth as session
from core.exceptions import DatabaseSavingException, DatabaseDeletingException

from ..domain import UserScope


class UserScopeRepo:
    __metaclass__ = ABCMeta

    @abstractmethod
    async def get_userscope(self, user_scope_id: int) -> Optional[UserScope]:
        pass

    @abstractmethod
    async def get_userscope_by(self, user_id: int, scope_id: int) -> Optional[UserScope]:
        pass

    @abstractmethod
    async def get_userscopes(self, user_id: int) -> list[UserScope]:
        pass

    @abstractmethod
    async def save_userscope(self, user_scope: UserScope) -> UserScope:
        pass

    @abstractmethod
    async def delete_userscope(self, user_scope: UserScope) -> None:
        pass

    @abstractmethod
    async def delete_userscopes(self, user_id: int) -> None:
        pass

    @abstractmethod
    async def commit_userscope(self) -> None:
        pass


class UserScopeSQLRepo(UserScopeRepo):
    async def get_userscope(self, user_scope_id: int) -> Optional[UserScope]:
        return await session.get(UserScope, user_scope_id)

    async def get_userscope_by(self, user_id: int, scope_id: int) -> Optional[UserScope]:
        result = await session.execute(
            select(UserScope).where(
                or_(
                    UserScope.user_id == user_id,
                    UserScope.scope_id == scope_id,
                )
            )
        )
        return result.scalars().first()

    async def get_userscopes(self, user_id: int) -> list[UserScope]:
        result = await session.execute(
            select(UserScope).where(
                or_(
                    UserScope.user_id == user_id,
                )
            )
        )
        return result.scalars().all()

    async def save_userscope(self, user_scope: UserScope) -> UserScope:
        try:
            session.add(user_scope)
            await session.commit()
            await session.refresh(user_scope)
            return user_scope
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseSavingException(f"Error saving userscope: {str(e)}")

    async def delete_userscope(self, user_scope: UserScope) -> None:
        try:
            await session.delete(user_scope)
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseDeletingException(f"Error deleting userscope: {str(e)}")

    async def delete_userscopes(self, user_id: int) -> None:
        try:
            await session.execute(delete(UserScope).where(UserScope.user_id == user_id))
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseDeletingException(f"Error deleting userscope: {str(e)}")

    async def commit_userscope(self) -> None:
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseDeletingException(f"Error commit userscope: {str(e)}")
