import os
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from contextvars import ContextVar, Token
from typing import Union
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_scoped_session,
)
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

from core import config
from .base import BaseCore as Base
from app._sys.changelog.domain import ChangeLog
from app._sys.crossorigin.domain import CrossOrigin
from app._sys.sysrepo.domain import SysRepo

session_context: ContextVar[str] = ContextVar("session_context_core")


def get_session_id() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


DB_FILE = ".db/system/core.db"
DB_ENGINE = "sqlite+aiosqlite:///" + DB_FILE
dbcore_engine = create_engine(DB_ENGINE.replace("+aiosqlite", ""))
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        f.write("")

if os.path.exists(DB_FILE):
    file_stats = os.stat(DB_FILE)
    if file_stats.st_size == 0:
        Base.metadata.create_all(bind=dbcore_engine)
        with dbcore_engine.begin() as connection:
            with Session(bind=connection) as db:
                db.add(
                    ChangeLog(
                        **{
                            "dateupdate": datetime.now(),
                            "version_name": "init",
                            "description": "Initial Commit",
                            "created_user": "SeMuT CiLiK",
                            "created_user": "SeMuT CiLiK",
                        }
                    )
                )
                db.add(
                    SysRepo(
                        **{
                            "name": "DBAPPS_LOCAL",
                            "allocation": "DBAPPS_URL_DEFAULT",
                            "datalink": "mysql+aiomysql://{user}:{password}@127.0.0.1:3307/db",
                            "user": "root",
                            "password": "password",
                            "is_active": True,
                            "created_user": "SeMuT CiLiK",
                        }
                    )
                )
                db.add(
                    SysRepo(
                        **{
                            "name": "DBAPPS_DEVELOPMENT",
                            "allocation": "DBAPPS_URL_DEFAULT",
                            "datalink": "mysql+aiomysql://{user}:{password}@127.0.0.1:3307/db",
                            "user": "root",
                            "password": "password",
                            "is_active": False,
                            "created_user": "SeMuT CiLiK",
                        }
                    )
                )
                db.add(
                    SysRepo(
                        **{
                            "name": "DBAPPS_PRODUCTION",
                            "allocation": "DBAPPS_URL_DEFAULT",
                            "datalink": "mysql+aiomysql://{user}:{password}@127.0.0.1:3307/db",
                            "user": "root",
                            "password": "password",
                            "is_active": False,
                            "created_user": "SeMuT CiLiK",
                        }
                    )
                )
                db.add(
                    SysRepo(
                        **{
                            "name": "RabbitMQ",
                            "allocation": "RabbitMQ",
                            "datalink": "amqp://{user}:{password}@192.168.40.5:5672//semut-dev",
                            "user": "guest",
                            "password": "guest",
                            "is_active": False,
                            "created_user": "SeMuT CiLiK",
                        }
                    )
                )
                db.add(CrossOrigin(**{"link": "http://localhost", "created_user": "init system"}))
                db.add(CrossOrigin(**{"link": "http://127.0.0.1", "created_user": "init system"}))
                db.add(CrossOrigin(**{"link": "http://127.0.0.1:8001", "created_user": "init system"}))
                db.commit()


async_engine = create_async_engine(DB_ENGINE)  # , echo=True)
async_session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

session_core: Union[AsyncSession, async_scoped_session] = async_scoped_session(
    session_factory=async_session,
    scopefunc=get_session_id,
)
