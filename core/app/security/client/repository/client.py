from typing import Optional, List, Union
from datetime import datetime

from abc import ABCMeta, abstractmethod
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from ..domain import Client
from core.db import session_security as session
from core.exceptions import DatabaseSavingException, DatabaseUpdatingException, DatabaseDeletingException


class ClientRepo:
    async def get_client(self, db: AsyncSession, client_id: int) -> Optional[Client]:
        return await db.get(Client, client_id)

    async def get_client_id(self, db: AsyncSession, client_id: str) -> Optional[Client]:
        result = await db.execute(select(Client).where(Client.client_id == client_id))
        return result.scalars().first()

    async def save_client(self, db: AsyncSession, client: Client) -> Client:
        try:
            db.add(client)
            await db.commit()
            await db.refresh(client)
            return client
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseSavingException(f"Error saving client: {str(e)}")

    async def update_client(self, db: AsyncSession, client: Client, **kwargs) -> None:
        try:
            for key, value in kwargs.items():
                if hasattr(client, key) and value is not None:
                    setattr(client, key, value)
            await db.commit()
            await db.refresh(client)
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseUpdatingException(f"Error updating client: {str(e)}")
