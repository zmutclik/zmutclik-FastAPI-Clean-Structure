from typing import Optional, List, Union
from datetime import datetime

from abc import ABCMeta, abstractmethod
from sqlalchemy import or_, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from ..domain import ClientUserOtp
from core.exceptions import DatabaseSavingException, DatabaseUpdatingException, DatabaseDeletingException


class ClientUserOTPRepo:
    async def get_clientuser_otp(self, db: AsyncSession, client_id: int, user: str) -> Optional[ClientUserOtp]:
        result = await db.execute(
            select(ClientUserOtp).where(
                ClientUserOtp.client_id == client_id,
                ClientUserOtp.user == user,
                ClientUserOtp.session_end >= func.now(),
                ClientUserOtp.active == True,
            )
        )
        return result.scalars().first()

    async def save_clientuser_otp(self, db: AsyncSession, clientuserotp: ClientUserOtp) -> ClientUserOtp:
        try:
            db.add(clientuserotp)
            await db.commit()
            await db.refresh(clientuserotp)
            return clientuserotp
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseSavingException(f"Error saving clientuserotp: {str(e)}")

    async def update_clientuser_otp(self, db: AsyncSession, clientuserotp: ClientUserOtp, **kwargs) -> None:
        try:
            for key, value in kwargs.items():
                if hasattr(clientuserotp, key) and value is not None:
                    setattr(clientuserotp, key, value)
            await db.commit()
            await db.refresh(clientuserotp)
            return clientuserotp
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseUpdatingException(f"Error updating clientuserotp: {str(e)}")
