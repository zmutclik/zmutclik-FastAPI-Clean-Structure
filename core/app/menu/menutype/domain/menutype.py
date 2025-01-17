import os

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time, TIMESTAMP, DateTime, func, case, Float, text
from sqlalchemy.orm import column_property, relationship, deferred, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from core.db.base import BaseMenu as Base
from core.db.mixins import TimestampLogMixin


class MenuType(Base, TimestampLogMixin):
    __tablename__ = "menutype"

    id = Column(Integer, primary_key=True, autoincrement=True)
    menutype = Column(String(64), unique=True)
    desc = Column(String(256))

    MENU = relationship("Menu", back_populates="MENUTYPE")

    @classmethod
    def create(cls, created_user: str, menutype: str, desc: str) -> "MenuType":
        return cls(menutype=menutype, desc=desc, created_user=created_user)
