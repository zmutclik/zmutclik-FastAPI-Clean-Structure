from typing import Optional, List, Union
from datetime import datetime
import time
from abc import ABCMeta, abstractmethod
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app._sys.logs.domain import Logs, IpAddress, RouterName
from core.exceptions import DatabaseSavingException, DatabaseUpdatingException, DatabaseDeletingException

from sqlalchemy.orm import Session


class LogsRepo:
    def __init__(self, tahunbulan: datetime = None) -> None:
        if tahunbulan is None:
            tahunbulan = datetime.now()
        self.db: Session = get_dblogs(tahunbulan).__next__()
        pass

    async def get_by_id(self, logs_id: int) -> Optional[Logs]:
        return await self.db.get(Logs, logs_id)

    def save(self, logs: Logs) -> Logs:
        try:
            self.db.add(logs)
            self.db.add(IpAddress(ipaddress=logs.ipaddress))
            self.db.add(RouterName(routername=logs.router))
            self.db.commit()

        except SQLAlchemyError as e:
            raise DatabaseSavingException(f"Error saving logs: {str(e)}")
