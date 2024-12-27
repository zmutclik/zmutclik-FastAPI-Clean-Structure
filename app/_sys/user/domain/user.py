import os

from sqlalchemy import Boolean, Column, ForeignKey, Integer, Unicode, String, Date, Time, TIMESTAMP, DateTime, func, case, Float, text
from sqlalchemy.orm import column_property, relationship, deferred, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from passlib.context import CryptContext

from core.db import BaseUser as Base
from core.db.mixins import TimestampLogMixin
from app._sys.user.exceptions.user import PasswordDoesNotMatchException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


class User(TimestampLogMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Unicode(32), unique=True)
    email = Column(Unicode(255), unique=True)
    nohp = Column(Unicode(32), unique=True)
    full_name = Column(Unicode(255))
    hashed_password = Column(Unicode(255))
    disabled = Column(Boolean, default=False)

    PRIVILEGE = relationship("Privilege", back_populates="USER")

    @hybrid_property
    def list_privilege(self) -> list[int]:
        res = []
        for item in self.PRIVILEGE:
            res.append(item.privilege)
        return res

    @classmethod
    def _is_password_match(cls, password1: str, password2: str) -> bool:
        return password1 == password2

    @classmethod
    def create(
        cls,
        username: str,
        password1: str,
        password2: str,
        email: str,
        nohp: str,
        full_name: str,
    ) -> "User":
        if not cls._is_password_match(password1=password1, password2=password2):
            raise PasswordDoesNotMatchException

        return cls(
            username=username,
            email=email,
            nohp=nohp,
            full_name=full_name,
            hashed_password=get_password_hash(password1),
        )

    def change_password(self, password1: str, password2: str) -> None:
        if not self._is_password_match(password1=password1, password2=password2):
            raise PasswordDoesNotMatchException

        self.password = get_password_hash(password1)
