from sqlalchemy import Boolean, Column, ForeignKey, BigInteger, Integer, Unicode, String, Date, Time, TIMESTAMP, DateTime, func, case, Float, text
from sqlalchemy.orm import column_property, relationship, deferred, Session

from core.db.base import BaseAuth as Base


class UserPrivilege(Base):
    __tablename__ = "user_privilege"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    privilege_id = Column(Integer, ForeignKey("privilege.id"))

    USER = relationship("User", back_populates="PRIVILEGE")
    PRIVILEGE = relationship("Privilege", back_populates="USERPRIVILEGE")

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
