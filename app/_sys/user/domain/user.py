import os

from sqlalchemy import Boolean, Column, ForeignKey, Integer, Unicode, String, Date, Time, TIMESTAMP, DateTime, func, case, Float, text
from sqlalchemy.orm import column_property, relationship, deferred, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from passlib.context import CryptContext

from core.db.base import BaseCore as Base
from core.db.mixins import TimestampLogMixin
from app._sys.user.exceptions.user import PasswordDoesNotMatchException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


class User(Base, TimestampLogMixin):
    __tablename__ = "_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32), unique=True)
    email = Column(String(255), unique=True)
    nohp = Column(String(32), unique=True)
    full_name = Column(String(255))
    hashed_password = Column(String(255), nullable=True)
    disabled = Column(Boolean, default=False)

    PRIVILEGE = relationship("UserPrivilege", back_populates="USER")

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
        created_user: str,
        username: str,
        password1: str,
        password2: str,
        email: str,
        nohp: str,
        full_name: str,
    ) -> "User":
        if not cls._is_password_match(password1=password1, password2=password2):
            raise PasswordDoesNotMatchException

        password = None if password1 is None else get_password_hash(password1)

        return cls(
            created_user=created_user,
            username=username,
            email=email,
            nohp=nohp,
            full_name=full_name,
            hashed_password=password,
        )

    def change_password(self, password1: str, password2: str) -> None:
        if not self._is_password_match(password1=password1, password2=password2):
            raise PasswordDoesNotMatchException

        self.password = get_password_hash(password1)

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.hashed_password)
