from sqlalchemy import Boolean, Column, ForeignKey, BigInteger, Integer, Unicode, String, Date, Time, TIMESTAMP, DateTime, func, case, Float, text
from sqlalchemy.orm import column_property, relationship, deferred, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from passlib.context import CryptContext

from core.db import Base


class UserPrivilege(Base):
    __tablename__ = "user_privilege"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    privilege_id = Column(Integer, ForeignKey("privilege.id"))

    USER = relationship("User", back_populates="PRIVILEGE")
    PRIVILEGE = relationship("Privilege", back_populates="USERPRIVILEGE")

    @hybrid_property
    def group(self) -> str:
        return self.PRIVILEGE.privilege

    @hybrid_property
    def desc(self) -> str:
        return self.PRIVILEGE.desc

    @classmethod
    def create(
        cls,
        user_id: int,
        privilege_id: int,
    ) -> "UserPrivilege":
        return cls(
            user_id=user_id,
            privilege_id=privilege_id,
        )
