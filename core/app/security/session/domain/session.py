import os
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Date,
    Time,
    TIMESTAMP,
    DateTime,
    func,
    case,
    Float,
    text,
)
from sqlalchemy.orm import column_property, relationship, deferred, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from core.db.base import BaseSecuriry as Base
from core.db.mixins import TimestampLogMixin


class Session(Base):
    __tablename__ = "session"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(String(64))
    session_id = Column(String(64), unique=True)
    user = Column(String(128), index=True)
    session_start = Column(DateTime, default=func.now())
    session_update = Column(DateTime, nullable=True)
    session_end = Column(DateTime)
    Lastipaddress = Column(String(50), index=True)
    LastPage = Column(String(256), nullable=True)
    active = Column(Boolean, default=True)

    @classmethod
    def create(
        cls,
        client_id: str,
        session_id: str,
        user: str,
        ipaddress: str,
        session_end: datetime,
    ) -> "Session":
        return cls(
            client_id=client_id,
            session_id=session_id,
            user=user,
            Lastipaddress=ipaddress,
            session_end=session_end,
        )
