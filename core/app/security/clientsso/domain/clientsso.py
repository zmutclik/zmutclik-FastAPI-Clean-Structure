import os, random, string
from datetime import datetime, timedelta, timezone
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time, TIMESTAMP, DateTime, func, case, Float, text
from sqlalchemy.orm import column_property, relationship, deferred, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from core.db.base import BaseSecuriry as Base
from core.db.mixins import TimestampLogMixin


class ClientSSO(Base, TimestampLogMixin):
    __tablename__ = "clientsso"

    clientsso_id = Column(String(64), primary_key=True, unique=True)
    clientsso_secret = Column(String(128))
    nama = Column(String(128))
    ipaddress = Column(String(64))
    callback_uri = Column(String(255))
    disabled = Column(Boolean, default=False)

    @classmethod
    def create(cls, clientsso_id: str, created_user: str, nama: str, ipaddress: str, callback_uri: str) -> "ClientSSO":
        return cls(
            created_user=created_user,
            clientsso_id=clientsso_id,
            clientsso_secret="".join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=16)),
            nama=nama,
            ipaddress=ipaddress,
            callback_uri=callback_uri,
        )


class ClientSSO_code(Base):
    __tablename__ = "clientsso_code"

    id = Column(Integer, primary_key=True, autoincrement=True)
    clientsso_id = Column(String(64))
    client_id = Column(String(64))
    code = Column(String(64))
    user_id = Column(Integer)
    session_end = Column(DateTime)

    @classmethod
    def create(cls, clientsso_id: str, client_id: str, code: str, user_id: int) -> "ClientSSO_code":
        session_end = datetime.now(timezone.utc) + timedelta(seconds=20)
        return cls(
            clientsso_id=clientsso_id,
            client_id=client_id,
            code=code,
            user_id=user_id,
            session_end=session_end,
        )
