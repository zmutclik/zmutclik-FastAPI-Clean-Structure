from typing import Optional, List, Union
from datetime import datetime

from abc import ABCMeta, abstractmethod
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from ..domain import AuthConfig
from core.db import session_core as session
from core.exceptions import DatabaseSavingException, DatabaseUpdatingException, DatabaseDeletingException


class AuthConfigRepo:

    __metaclass__ = ABCMeta

    @abstractmethod
    async def get(self) -> Optional[AuthConfig]:
        pass

    @abstractmethod
    async def update(self, authconfig: AuthConfig, **kwargs) -> AuthConfig:
        pass


class AuthConfigSQLRepo(AuthConfigRepo):
    async def get(self) -> Optional[AuthConfig]:
        result = await session.execute(select(AuthConfig))
        return result.scalars().first()

    async def update(self, authconfig: AuthConfig, **kwargs) -> AuthConfig:
        try:
            for key, value in kwargs.items():
                if hasattr(authconfig, key) and value is not None:
                    setattr(authconfig, key, value)
            await session.commit()
            await session.refresh(authconfig)
            return authconfig
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseUpdatingException(f"Error updating authconfig: {str(e)}")
