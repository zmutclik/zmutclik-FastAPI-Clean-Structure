from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time, TIMESTAMP, DateTime, func, case, Float, text, Text

from core.db.base import BaseMessage as Base
from core.db.mixins import TimestampLogMixin
from core import config


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime)
    device = Column(String(32), index=True)
    sender = Column(String(32), index=True)
    target = Column(String(32), index=True)
    text = Column(Text)
    status = Column(String(32), index=True)
    state = Column(String(32), index=True, nullable=True)

    @classmethod
    def create(
        cls,
        device: str,
        sender: str,
        target: str,
        text: str,
    ) -> "Message":

        return cls(
            timestamp=datetime.now(),
            device=device,
            sender=sender,
            target=target,
            text=text,
            status="created",
        )
