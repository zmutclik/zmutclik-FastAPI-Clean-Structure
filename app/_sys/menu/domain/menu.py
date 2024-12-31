import os

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time, TIMESTAMP, DateTime, func, case, Float, text
from sqlalchemy.orm import column_property, relationship, deferred, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from core.db import Base
from core.db.mixins import TimestampLogMixin


class Menu(Base, TimestampLogMixin):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, autoincrement=True)

    text = Column(String(128), unique=True)
    segment = Column(String(128), index=True)
    tooltip = Column(String(256))
    href = Column(String(256))
    icon = Column(String(256))
    icon_color = Column(String(32))

    sort = Column(Integer, default=0)
    menutype_id = Column(Integer, ForeignKey("menuType.id"))
    parent_id = Column(Integer, ForeignKey("menu.id"), default=0)
    disabled = Column(Boolean, default=False)

    MENUTYPE = relationship("MenuType", back_populates="MENU")
    CHILDREN = relationship("Menu", back_populates="PARENT")
    PARENT = relationship("Menu", back_populates="CHILDREN", remote_side=[id])

    @classmethod
    def create(
        cls,
        text: str,
        segment: str,
        tooltip: str,
        href: str,
        icon: str,
        icon_color: str,
        menutype_id: int,
    ) -> "Menu":
        return cls(
            text=text,
            segment=segment,
            tooltip=tooltip,
            href=href,
            icon=icon,
            icon_color=icon_color,
            menutype_id=menutype_id,
        )
