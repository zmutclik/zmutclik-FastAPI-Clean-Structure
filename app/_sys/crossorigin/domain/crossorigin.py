import os

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time, TIMESTAMP, DateTime, func, case, Float, text
from sqlalchemy.orm import column_property, relationship, deferred, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from core.db import Base
from core.db.mixins import TimestampLogMixin


class CrossOrigin(Base, TimestampLogMixin):
    __tablename__ = "sys_cross_origin"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    link = Column(String(64), unique=True, index=True)

    @classmethod
    def create(cls, link: str) -> "CrossOrigin":
        return cls(link=link)
