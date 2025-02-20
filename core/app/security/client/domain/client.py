from datetime import datetime, timedelta, timezone
import random

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
    OTP = relationship("ClientUserOtp", back_populates="CLIENT")

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


class ClientUserResetCode(Base):
    __tablename__ = "client_user_reset_code"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String(128), nullable=False, index=True)
    salt = Column(String(64), nullable=False)
    code = Column(String(12), nullable=False)
    session_end = Column(DateTime, nullable=False)
    active = Column(Boolean, default=True)

    @classmethod
    def create(cls, user: str, code: str, salt: str) -> "ClientUserResetCode":
        session_end = datetime.now(timezone.utc) + timedelta(minutes=15)
        return cls(
            user=user,
            code=code,
            salt=salt,
            session_end=session_end,
            active=True,
        )


def generate_adjacent_same_digits():
    repeated_digit = str(random.randint(0, 9))
    other_digits = random.sample([str(i) for i in range(10) if str(i) != repeated_digit], 2)
    positions = [0, 1, 2]
    pos = random.choice(positions)
    digits = other_digits[:pos] + [repeated_digit, repeated_digit] + other_digits[pos:]
    data = int("".join(digits))
    if len(str(data)) != 4:
        return generate_adjacent_same_digits()
    return data


class ClientUserOtp(Base):
    __tablename__ = "client_user_otp"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("client.id"))
    user = Column(String(128), nullable=False, index=True)
    otp = Column(Integer, nullable=False)
    loggedin = Column(DateTime, nullable=True)
    session_start = Column(DateTime, default=func.now())
    session_end = Column(DateTime)
    active = Column(Boolean, default=True)

    CLIENT = relationship("Client", back_populates="OTP")

    @classmethod
    def create(cls, client_id: int, user: str, session_end: datetime) -> "ClientUserOtp":
        return cls(
            client_id=client_id,
            user=user,
            session_end=session_end,
            otp=generate_adjacent_same_digits(),
        )
