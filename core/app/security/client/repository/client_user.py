from typing import Optional, List, Union
from datetime import datetime

from abc import ABCMeta, abstractmethod
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from ..domain import ClientUser
from core.db import session_security as session
from core.exceptions import DatabaseSavingException, DatabaseUpdatingException, DatabaseDeletingException


class ClientUserRepo:
    async def get_clientuser(self, db: AsyncSession, client_id: int, user: str) -> Optional[ClientUser]:
        result = await db.execute(select(ClientUser).where(ClientUser.client_id == client_id, ClientUser.user == user))
        return result.scalars().first()

    async def get_clientusers(self, db: AsyncSession, client_id: int) -> Optional[ClientUser]:
        result = await db.execute(select(ClientUser).where(ClientUser.client_id == client_id).order_by(ClientUser.user))
        return result.scalars().all()

    async def save_clientuser(self, db: AsyncSession, clientuser: ClientUser) -> ClientUser:
        try:
            db.add(clientuser)
            await db.commit()
            await db.refresh(clientuser)
            return clientuser
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseSavingException(f"Error saving clientuser: {str(e)}")

    async def update_clientuser(self, db: AsyncSession, clientuser: ClientUser, **kwargs) -> None:
        try:
            for key, value in kwargs.items():
                if hasattr(clientuser, key) and value is not None:
                    setattr(clientuser, key, value)
            await db.commit()
            await db.refresh(clientuser)
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseUpdatingException(f"Error updating clientuser: {str(e)}")
