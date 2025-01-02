from typing import Optional, List, Union
from datetime import datetime

from abc import ABCMeta, abstractmethod
from sqlalchemy import or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app._sys.crossorigin.domain import CrossOrigin
from core.db import engine_dbsys
from core.exceptions import DatabaseSavingException, DatabaseUpdatingException, DatabaseDeletingException


class CrossOriginRepo:

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_sys(self) -> list:
        pass

    @abstractmethod
    def get(self, link: str) -> Optional[CrossOrigin]:
        pass

    @abstractmethod
    def get_by_id(self, crossorigin_id: int) -> Optional[CrossOrigin]:
        pass

    @abstractmethod
    def save(self, crossorigin: CrossOrigin) -> CrossOrigin:
        pass

    @abstractmethod
    def update(self, crossorigin: CrossOrigin, **kwargs) -> CrossOrigin:
        pass

    @abstractmethod
    def delete(self, crossorigin: CrossOrigin, deleted_user: str) -> None:
        pass


class CrossOriginSQLRepo(CrossOriginRepo):
    def get_sys(self):
        with engine_dbsys.begin() as connection:
            with Session(bind=connection) as db:
                result = db.execute(select(CrossOrigin))
                res = []
                for item in result.scalars().all():
                    res.append(item)
                return res

    def get(self, link: str) -> Optional[CrossOrigin]:
        with engine_dbsys.begin() as connection:
            with Session(bind=connection) as db:
                result = db.execute(select(CrossOrigin).where(CrossOrigin.link == link))
                return result.scalars().first()

    def get_by_id(self, crossorigin_id: int) -> Optional[CrossOrigin]:
        with engine_dbsys.begin() as connection:
            with Session(bind=connection) as db:
                return db.get(CrossOrigin, crossorigin_id)

    def save(self, crossorigin: CrossOrigin) -> CrossOrigin:
        with engine_dbsys.begin() as connection:
            with Session(bind=connection) as db:
                try:
                    db.add(crossorigin)
                    db.commit()
                    db.refresh(crossorigin)
                    return crossorigin
                except SQLAlchemyError as e:
                    db.rollback()
                    raise DatabaseSavingException(f"Error saving crossorigin: {str(e)}")

    def update(self, crossorigin: CrossOrigin, **kwargs) -> CrossOrigin:
        with engine_dbsys.begin() as connection:
            with Session(bind=connection) as db:
                try:
                    for key, value in kwargs.items():
                        if hasattr(crossorigin, key) and value is not None:
                            setattr(crossorigin, key, value)
                    db.commit()
                    db.refresh(crossorigin)
                    return crossorigin
                except SQLAlchemyError as e:
                    db.rollback()
                    raise DatabaseUpdatingException(f"Error updating crossorigin: {str(e)}")

    def delete(self, crossorigin: CrossOrigin, deleted_user: str) -> None:
        with engine_dbsys.begin() as connection:
            with Session(bind=connection) as db:
                try:
                    if not crossorigin.deleted_at:
                        crossorigin.deleted_at = datetime.now()
                        crossorigin.deleted_user = deleted_user
                        db.commit()
                except SQLAlchemyError as e:
                    db.rollback()
                    raise DatabaseDeletingException(f"Error deleting crossorigin: {str(e)}")
