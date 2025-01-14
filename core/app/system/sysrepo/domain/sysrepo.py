import os
from datetime import date

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time, TIMESTAMP, DateTime, func, case, Float, text
from sqlalchemy.orm import column_property, relationship, deferred, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from core.db.base import BaseCore as Base
from core.db.mixins import TimestampLogMixin


class SysRepo(Base, TimestampLogMixin):
    __tablename__ = "repository"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    allocation = Column(String(255), nullable=False)
    datalink = Column(String(255), nullable=False)
    user = Column(String(64))
    password = Column(String(64))
    is_active = Column(Boolean, default=False)

    @classmethod
    def create(
        cls,
        name: str,
        allocation: str,
        datalink: str,
        user: str,
        password: str,
    ) -> "SysRepo":

        return cls(
            name=name,
            allocation=allocation,
            datalink=datalink,
            user=user,
            password=password,
        )
