import os

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time, TIMESTAMP, DateTime, func, case, Float, text
from sqlalchemy.orm import column_property, relationship, deferred, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from core.db.base import BaseSecuriry as Base
from core.db.mixins import TimestampLogMixin


class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(String(64), unique=True)
    platform = Column(String(100), index=True)
    browser = Column(String(100), index=True)
    disabled = Column(Boolean, default=False)

    USERS = relationship("ClientUser", back_populates="CLIENT")

    @classmethod
    def create(cls, client_id: str, platform: str, browser: str) -> "Client":
        return cls(
            client_id=client_id,
            platform=platform,
            browser=browser,
        )


class ClientUser(Base):
    __tablename__ = "client_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("client.id"))
    user = Column(String(128), nullable=False, index=True)
    LastLogin = Column(DateTime, nullable=True)
    LastPage = Column(String(256), nullable=True)
    Lastipaddress = Column(String(50), index=True)

    CLIENT = relationship("Client", back_populates="USERS")

    @classmethod
    def create(cls, client_id: int, user: str) -> "ClientUser":
        return cls(
            client_id=client_id,
            user=user,
        )
