from sqlalchemy import Column, DateTime, func, Unicode
from sqlalchemy.ext.declarative import declared_attr


class TimestampLogMixin:
    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=func.now(), nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime,
            default=func.now(),
            onupdate=func.now(),
            nullable=False,
        )

    @declared_attr
    def deleted_at(cls):
        return Column(DateTime, default=None, nullable=True)

    @declared_attr
    def created_user(cls):
        return Column(Unicode(255), nullable=False)

    @declared_attr
    def deleted_user(cls):
        return Column(Unicode(255), default=None, nullable=True)
