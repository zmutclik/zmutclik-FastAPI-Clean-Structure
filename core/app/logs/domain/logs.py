import os
import time
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time, TIMESTAMP, DateTime, func, case, Float, text
from sqlalchemy.orm import column_property, relationship, deferred, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from fastapi import Request
from user_agents import parse

from core.db.base import BaseLogs as Base
from core.db.mixins import TimestampLogMixin
from core import config


class Logs(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(String(32), index=True)
    session_id = Column(String(32), index=True)
    startTime = Column(Float)
    app = Column(String(100), index=True)
    channel = Column(String(32), index=True)
    platform = Column(String(100), index=True)
    browser = Column(String(100), index=True)
    referer = Column(String(500), index=True)
    router = Column(String(256), nullable=True, index=True)
    path = Column(String(256), index=True)
    method = Column(String(10), index=True)
    ipaddress = Column(String(50), index=True)
    ipproxy = Column(String(50), nullable=True, index=True)
    user = Column(String(128), nullable=True, index=True)
    status_code = Column(Integer, nullable=True, index=True)
    process_time = Column(Float, nullable=True)

    @classmethod
    def create(
        cls,
        request: Request,
    ) -> "Logs":
        try:
            user_agent = parse(request.headers.get("user-agent"))
            platform = user_agent.os.family + user_agent.os.version_string
            browser = user_agent.browser.family + user_agent.browser.version_string
        except:
            platform = ""
            browser = ""

        ipaddress = request.client.host
        ipproxy = None
        try:
            if request.headers.get("X-Real-IP") is not None:
                ipaddress = request.headers.get("X-Real-IP")
                ipproxy = request.client.host
        except:
            pass

        return cls(
            startTime=time.time(),
            app=config.APP_NAME,
            channel=request.user.channel,
            client_id=request.user.client_id,
            platform=platform,
            browser=browser,
            referer=request.headers.get("referer"),
            path=request.scope["path"],
            method=request.method,
            ipaddress=ipaddress,
            ipproxy=ipproxy,
        )


class IpAddress(Base):
    __tablename__ = "logs_ipaddress"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ipaddress = Column(String(50), index=True)


class RouterName(Base):
    __tablename__ = "logs_router"
    id = Column(Integer, primary_key=True, autoincrement=True)
    routername = Column(String(255), index=True)


class UserName(Base):
    __tablename__ = "logs_username"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), index=True)


class ClientID(Base):
    __tablename__ = "logs_clientid"
    id = Column(Integer, primary_key=True, autoincrement=True)
    clientid = Column(String(255), index=True)
    username = Column(String(255), index=True)
    platform = Column(String(100), index=True)
    browser = Column(String(100), index=True)
