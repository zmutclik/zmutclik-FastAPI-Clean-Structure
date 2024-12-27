from sqlalchemy.ext.declarative import declarative_base
from .session import session

__all__ = [
    "session",
]

Base = declarative_base()
BaseLogs = declarative_base()
BaseUser = declarative_base()
BaseSysT = declarative_base()
BaseSeSS = declarative_base()
