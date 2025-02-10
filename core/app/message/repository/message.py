from typing import Optional, List, Union
from datetime import datetime

from sqlalchemy import or_, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from ..domain import Message
from core.exceptions import DatabaseSavingException, DatabaseUpdatingException


class MessageRepo:
    async def get_message(self, db: AsyncSession, id: int) -> Optional[Message]:
        return await db.get(Message, id)

    async def save_message(self, db: AsyncSession, message: Message) -> Message:
        try:
            db.add(message)
            await db.commit()
            await db.refresh(message)
            return message
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseSavingException(f"Error saving message: {str(e)}")

    async def update_message(self, db: AsyncSession, message: Message, **kwargs) -> Message:
        try:
            for key, value in kwargs.items():
                if hasattr(message, key) and value is not None:
                    setattr(message, key, value)
            await db.commit()
            await db.refresh(message)
            return message
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseUpdatingException(f"Error updating message: {str(e)}")
