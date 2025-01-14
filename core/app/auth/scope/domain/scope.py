import os

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time, TIMESTAMP, DateTime, func, case, Float, text
from sqlalchemy.orm import column_property, relationship, deferred, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from core.db.base import BaseAuth as Base
from core.db.mixins import TimestampLogMixin


class Scope(Base, TimestampLogMixin):
    __tablename__ = "scope"

    id = Column(Integer, primary_key=True, autoincrement=True)
    scope = Column(String(64), unique=True)
    desc = Column(String(255))

    USERSCOPE = relationship("UserScope", back_populates="SCOPE")

    @classmethod
    def create(cls, scope: str, desc: str) -> "Scope":
        return cls(scope=scope, desc=desc)
