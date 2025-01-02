from typing import Optional, List, Union
from datetime import datetime

from abc import ABCMeta, abstractmethod
from fastapi import Depends
from sqlalchemy import or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app._sys.crossorigin.domain import CrossOrigin
from core.db import engine_dbsys, get_dbsys, SessionLocalSys
from core.exceptions import DatabaseSavingException, DatabaseUpdatingException, DatabaseDeletingException


class CrossOriginRepo:

    __metaclass__ = ABCMeta
    db = Session

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
    # def __init__(self, db: Session = None):
    #     print("create")
    #     self.db = db or SessionLocalSys()

    def __enter__(self):
        print("enter")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # if exc_type is not None:
        #     self.db.rollback()
        # self.db.close()
        print("close")

    def get_sys(self):
        with engine_dbsys.begin() as connection:
            with Session(bind=connection) as db:
                result = db.execute(select(CrossOrigin))
                res = []
                for item in result.scalars().all():
                    res.append(item)
                if res == []:
                    res.append("*")
                return res

    def get(self, link: str) -> Optional[CrossOrigin]:
        # with engine_dbsys.begin() as connection:
        #     with Session(bind=connection) as db:
        result = self.db.execute(select(CrossOrigin).where(CrossOrigin.link == link))
        return result.scalars().first()

    def get_by_id(self, crossorigin_id: int) -> Optional[CrossOrigin]:
        # with engine_dbsys.begin() as connection:
        #     with Session(bind=connection) as db:
        return self.db.get(CrossOrigin, crossorigin_id)

    def save(self, crossorigin: CrossOrigin) -> CrossOrigin:
        # with engine_dbsys.begin() as connection:
        #     with Session(bind=connection) as db:
        try:
            self.db.add(crossorigin)
            self.db.commit()
            self.db.refresh(crossorigin)
            return crossorigin
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseSavingException(f"Error saving crossorigin: {str(e)}")

    def update(self, crossorigin: CrossOrigin, **kwargs) -> CrossOrigin:
        # with engine_dbsys.begin() as connection:
        #     with Session(bind=connection) as db:
        try:
            for key, value in kwargs.items():
                if hasattr(crossorigin, key) and value is not None:
                    setattr(crossorigin, key, value)
            self.db.commit()
            self.db.refresh(crossorigin)
            return crossorigin
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseUpdatingException(f"Error updating crossorigin: {str(e)}")

    def delete(self, crossorigin: CrossOrigin, deleted_user: str) -> None:
        # with engine_dbsys.begin() as connection:
        #     with Session(bind=connection) as db:
        try:
            if not crossorigin.deleted_at:
                crossorigin.deleted_at = datetime.now()
                crossorigin.deleted_user = deleted_user
                self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseDeletingException(f"Error deleting crossorigin: {str(e)}")
