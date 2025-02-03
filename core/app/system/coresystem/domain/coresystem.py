import os

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time, TIMESTAMP, DateTime, func, case, Float, text
from sqlalchemy.orm import column_property, relationship, deferred, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from core.db.base import BaseCore as Base


class CoreSYSTEM(Base):
    __tablename__ = "coresystem"

    environment = Column(String(256), primary_key=True)
    app_name = Column(String(256))
    app_desc = Column(String(256))
    app_host = Column(String(256))
    app_port = Column(Integer)
    debug = Column(Boolean)
