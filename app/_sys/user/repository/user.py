from typing import Optional, List, Union
from datetime import datetime

from abc import ABCMeta, abstractmethod
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from core.db import session
from core.exceptions import DatabaseSavingException, DatabaseUpdatingException, DatabaseDeletingException

from app._sys.user.domain import User


class UserRepo:
    __metaclass__ = ABCMeta
    
    @abstractmethod
    async def get(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by(
        self,
        username: Union[str, None],
        email: Union[str, None],
        nohp: Union[str, None],
    ) -> Optional[User]:
        pass

    @abstractmethod
    async def save(self, user: User) -> User:
        pass

    @abstractmethod
    async def update(self, user: User, **kwargs) -> User:
        pass

    @abstractmethod
    async def delete(self, user: User, deleted_user: str) -> None:
        pass


class UserSQLRepo(UserRepo):
    async def get(self, user_id: int) -> Optional[User]:
        return await session.get(User, user_id)

    async def get_by(
        self,
        username: Union[str, None] = None,
        email: Union[str, None] = None,
        nohp: Union[str, None] = None,
    ) -> Optional[User]:
        filters = []
        if username:
            filters.append(User.username == username)
        if email:
            filters.append(User.email == email)
        if nohp:
            filters.append(User.nohp == nohp)

        if not filters:
            return None

        result = await session.execute(select(User).where(or_(*filters)))

        return result.scalars().first()

    async def save(self, user: User) -> User:
        try:
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseSavingException(f"Error saving user: {str(e)}")

    async def update(self, user: User, **kwargs) -> User:
        try:
            for key, value in kwargs.items():
                if hasattr(user, key) and value is not None:
                    setattr(user, key, value)
            await session.commit()
            await session.refresh(user)
            return user
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseUpdatingException(f"Error updating user: {str(e)}")

    async def delete(self, user: User, deleted_user: str) -> None:
        try:
            if not user.deleted_at:
                user.deleted_at = datetime.now()
                user.deleted_user = deleted_user
                await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseDeletingException(f"Error deleting user: {str(e)}")
