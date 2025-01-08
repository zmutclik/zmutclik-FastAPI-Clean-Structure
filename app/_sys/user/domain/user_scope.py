from sqlalchemy import Boolean, Column, ForeignKey, BigInteger, Integer, Unicode, String, Date, Time, TIMESTAMP, DateTime, func, case, Float, text
from sqlalchemy.orm import column_property, relationship, deferred, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from passlib.context import CryptContext

from core.db.base import BaseCore as Base


class UserScope(Base):
    __tablename__ = "_user_scope"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("_user.id"))
    scope_id = Column(Integer, ForeignKey("_scope.id"))

    USER = relationship("User", back_populates="SCOPE")
    SCOPE = relationship("Scope", back_populates="USERSCOPE")

    @hybrid_property
    def group(self) -> str:
        return self.SCOPE.scope

    @hybrid_property
    def desc(self) -> str:
        return self.SCOPE.desc

    @classmethod
    def create(
        cls,
        user_id: int,
        scope_id: int,
    ) -> "UserScope":
        return cls(
            user_id=user_id,
            scope_id=scope_id,
        )
