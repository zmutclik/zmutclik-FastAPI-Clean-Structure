from sqlalchemy import Boolean, Column, ForeignKey, BigInteger, Integer, Unicode, String, Date, Time, TIMESTAMP, DateTime, func, case, Float, text
from sqlalchemy.orm import column_property, relationship, deferred, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from passlib.context import CryptContext

from core.db.base import BaseAuth as Base


class PrivilegeMenus(Base):
    __tablename__ = "privilege_menus"

    id = Column(Integer, primary_key=True, autoincrement=True)
    privilege_id = Column(Integer, ForeignKey("privilege.id"))
    menutype_id = Column(Integer, index=True)
    menu_id = Column(Integer, index=True)

    PRIVILEGE = relationship("Privilege", back_populates="PRIVILEGEMENUS")

    @classmethod
    def create(cls, privilege_id: int, menutype_id: int, menu_id: int) -> "PrivilegeMenus":
        return cls(privilege_id=privilege_id, menutype_id=menutype_id, menu_id=menu_id)
