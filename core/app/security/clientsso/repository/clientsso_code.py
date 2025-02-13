from typing import Optional, List, Union
from datetime import datetime

from abc import ABCMeta, abstractmethod
from sqlalchemy import or_, select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from ..domain import ClientSSO_code
from core.db import session
from core.exceptions import DatabaseSavingException, DatabaseUpdatingException, DatabaseDeletingException


class ClientSSOCodeRepo:
    async def get_clientsso_code(self, db: AsyncSession, clientsso_id: str, code: str) -> Optional[ClientSSO_code]:
        result = await db.execute(
            select(ClientSSO_code).where(
                ClientSSO_code.clientsso_id == clientsso_id,
                ClientSSO_code.code == code,
                ClientSSO_code.session_end >= func.now(),
            )
        )
        return result.scalars().first()

    async def get_clientsso_findcode(self, db: AsyncSession, code: str) -> Optional[ClientSSO_code]:
        result = await db.execute(
            select(ClientSSO_code).where(
                ClientSSO_code.code == code,
                ClientSSO_code.session_end >= func.now(),
            )
        )
        return result.scalars().first()

    async def save_clientsso_code(self, db: AsyncSession, clientsso_code: ClientSSO_code) -> ClientSSO_code:
        try:
            db.add(clientsso_code)
            await db.commit()
            await db.refresh(clientsso_code)
            return clientsso_code
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseSavingException(f"Error saving clientsso code: {str(e)}")

    async def delete_clientsso_code(self, db: AsyncSession, client_id: str) -> None:
        try:
            await db.execute(delete(ClientSSO_code).where(ClientSSO_code.client_id == client_id))
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseDeletingException(f"Error deleting clientsso code: {str(e)}")
