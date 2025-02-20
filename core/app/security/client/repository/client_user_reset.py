from typing import Optional, List, Union
from datetime import datetime

from abc import ABCMeta, abstractmethod
from sqlalchemy import or_, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from ..domain import ClientUserResetCode
from core.exceptions import DatabaseSavingException, DatabaseUpdatingException, DatabaseDeletingException


class ClientUserResetCodeRepo:
    async def get_clientuser_reset_code(self, db: AsyncSession, user: str, code: str) -> Optional[ClientUserResetCode]:
        result = await db.execute(
            select(ClientUserResetCode).where(
                ClientUserResetCode.user == user,
                ClientUserResetCode.code == code,
            )
        )
        return result.scalars().first()

    async def get_clientuser_reset_salt(self, db: AsyncSession, user: str, salt: str) -> Optional[ClientUserResetCode]:
        result = await db.execute(
            select(ClientUserResetCode).where(
                ClientUserResetCode.user == user,
                ClientUserResetCode.salt == salt,
            )
        )
        return result.scalars().first()

    async def get_clientuser_reset(self, db: AsyncSession, user: str) -> Optional[ClientUserResetCode]:
        result = await db.execute(
            select(ClientUserResetCode).where(
                ClientUserResetCode.user == user,
                ClientUserResetCode.session_end >= func.now(),
                ClientUserResetCode.active == True,
            )
        )
        return result.scalars().first()

    async def get_clientuser_reset_by_salt(self, db: AsyncSession, salt: str) -> Optional[ClientUserResetCode]:
        result = await db.execute(
            select(ClientUserResetCode).where(
                ClientUserResetCode.salt == salt,
                ClientUserResetCode.session_end >= func.now(),
                ClientUserResetCode.active == True,
            )
        )
        return result.scalars().first()

    async def save_clientuser_reset(self, db: AsyncSession, clientuserreset: ClientUserResetCode) -> ClientUserResetCode:
        try:
            db.add(clientuserreset)
            await db.commit()
            await db.refresh(clientuserreset)
            return clientuserreset
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseSavingException(f"Error saving clientuserresetcode: {str(e)}")

    async def update_clientuser_reset(self, db: AsyncSession, clientuserreset: ClientUserResetCode, **kwargs) -> None:
        try:
            for key, value in kwargs.items():
                if hasattr(clientuserreset, key) and value is not None:
                    setattr(clientuserreset, key, value)
            await db.commit()
            await db.refresh(clientuserreset)
            return clientuserreset
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseUpdatingException(f"Error updating clientuserresetcode: {str(e)}")
