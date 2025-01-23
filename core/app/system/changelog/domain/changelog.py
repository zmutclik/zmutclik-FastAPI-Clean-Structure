import os
from datetime import date

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time, TIMESTAMP, DateTime, func, case, Float, text
from sqlalchemy.orm import column_property, relationship, deferred, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from core.db.base import BaseCore as Base
from core.db.mixins import TimestampLogMixin


class ChangeLog(Base, TimestampLogMixin):
    __tablename__ = "changelog"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dateupdate = Column(Date, nullable=False)
    version_name = Column(String(50), unique=True)
    description = Column(String(256))

    @classmethod
    def create(
        cls,
        created_user: str,
        dateupdate: date,
        version_name: str,
        description: str,
    ) -> "ChangeLog":

        return cls(
            created_user=created_user,
            dateupdate=dateupdate,
            version_name=version_name,
            description=description,
        )
