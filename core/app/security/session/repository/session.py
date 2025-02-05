from typing import Optional, List, Union
from datetime import datetime

from abc import ABCMeta, abstractmethod
from sqlalchemy import or_, select,func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from ..domain import Session
from core.exceptions import DatabaseSavingException, DatabaseUpdatingException


class SessionRepo:
    async def get_session(self, db: AsyncSession, id: int) -> Optional[Session]:
        return await db.get(Session, id)

    async def get_session_id(self, db: AsyncSession, session_id: str) -> Optional[Session]:
        result = await db.execute(select(Session).where(Session.session_id == session_id, Session.session_end >= func.now(), Session.active == True))
        return result.scalars().first()

    async def save_session(self, db: AsyncSession, session: Session) -> Session:
        try:
            db.add(session)
            await db.commit()
            await db.refresh(session)
            return session
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseSavingException(f"Error saving session: {str(e)}")

    async def update_session(self, db: AsyncSession, data_session: Session, **kwargs) -> Session:
        try:
            for key, value in kwargs.items():
                if hasattr(data_session, key) and value is not None:
                    setattr(data_session, key, value)
            await db.commit()
            await db.refresh(data_session)
            return data_session
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseUpdatingException(f"Error updating session: {str(e)}")
