import os
from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time, TIMESTAMP, DateTime, func, case, Float, text
from sqlalchemy.orm import column_property, relationship, deferred, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from core.db.base import BaseAuth as Base
from core.db.mixins import TimestampLogMixin


class Privilege(Base, TimestampLogMixin):
    __tablename__ = "privilege"

    id = Column(Integer, primary_key=True, autoincrement=True)
    privilege = Column(String(64), unique=True)
    desc = Column(String(255))

    USERPRIVILEGE = relationship("UserPrivilege", back_populates="PRIVILEGE")
    PRIVILEGEMENUS = relationship("PrivilegeMenus", back_populates="PRIVILEGE")

    @classmethod
    def create(cls, created_user: str, privilege: str, desc: str) -> "Privilege":
        return cls(privilege=privilege, desc=desc, created_user=created_user)
