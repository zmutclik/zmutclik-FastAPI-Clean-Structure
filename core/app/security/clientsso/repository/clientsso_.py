from typing import Optional, List, Union
from datetime import datetime

from abc import ABCMeta, abstractmethod
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from ..domain import ClientSSO
from core.db import session
from core.exceptions import DatabaseSavingException, DatabaseUpdatingException, DatabaseDeletingException


class ClientSSORepo:
    async def get_clientsso(self, db: AsyncSession, clientsso_id: str) -> Optional[ClientSSO]:
        result = await db.execute(
            select(ClientSSO).where(
                ClientSSO.clientsso_id == clientsso_id,
                ClientSSO.deleted_at == None,
                ClientSSO.disabled == False,
            )
        )
        return result.scalars().first()

    async def save_clientsso(self, db: AsyncSession, clientsso: ClientSSO) -> ClientSSO:
        try:
            db.add(clientsso)
            await db.commit()
            await db.refresh(clientsso)
            return clientsso
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseSavingException(f"Error saving clientsso: {str(e)}")

    async def update_clientsso(self, db: AsyncSession, clientsso: ClientSSO, **kwargs) -> ClientSSO:
        try:
            for key, value in kwargs.items():
                if hasattr(clientsso, key) and value is not None:
                    setattr(clientsso, key, value)
            await db.commit()
            await db.refresh(clientsso)
            return clientsso
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseUpdatingException(f"Error updating clientsso: {str(e)}")

    async def delete_clientsso(self, db: AsyncSession, clientsso: ClientSSO, deleted_user: str) -> None:
        try:
            if not clientsso.deleted_at:
                clientsso.deleted_at = datetime.now()
                clientsso.deleted_user = deleted_user
                await db.commit()
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseDeletingException(f"Error deleting clientsso: {str(e)}")
