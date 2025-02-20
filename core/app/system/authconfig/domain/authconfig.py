import os

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time, TIMESTAMP, DateTime, func, case, Float, text
from sqlalchemy.orm import column_property, relationship, deferred, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from core.db.base import BaseCore as Base
from core.db.mixins import TimestampLogMixin


class AuthConfig(Base):
    __tablename__ = "authconfig"

    sso_login_url = Column(String(256))
    sso_token_url = Column(String(256))
    sso_client_id = Column(String(256), primary_key=True)
    jwt_scret_key = Column(String(256))
    jwt_algorithm = Column(String(256))
    cookies_prefix = Column(String(256))
    cookies_https = Column(Boolean)
    cookies_exp = Column(Integer)
    refresh_exp = Column(Integer)
    timeout_exp = Column(Integer)
    register_account = Column(Boolean)
