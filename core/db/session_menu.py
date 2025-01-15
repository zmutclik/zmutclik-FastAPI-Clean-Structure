import os
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
from .base import BaseMenu as Base
from core.app.menu.menu.domain import Menu
from core.app.menu.menutype.domain import MenuType

session_context: ContextVar[str] = ContextVar("session_context_menu")


def get_session_id() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


DB_FILE = ".db/system/menu.db"
DB_ENGINE = "sqlite+aiosqlite:///" + DB_FILE
dbmenu_engine = create_engine(DB_ENGINE.replace("+aiosqlite", ""))
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        f.write("")

if os.path.exists(DB_FILE):
    file_stats = os.stat(DB_FILE)
    if file_stats.st_size == 0:
        Base.metadata.create_all(bind=dbmenu_engine)
        with dbmenu_engine.begin() as connection:
            with Session(bind=connection) as db:
                db.add(
                    MenuType(
                        **{
                            "menutype": "sidebar",
                            "desc": "Side Bar Menu",
                            "created_user": "init system",
                        }
                    )
                )
                db.add(
                    Menu(
                        **{
                            "text": "Dashboard",
                            "href": "/page/dashboard",
                            "segment": "dashboard",
                            "icon": "fas fa-tachometer-alt",
                            "icon_color": "",
                            "sort": 1,
                            "menutype_id": 1,
                            "parent_id": 0,
                            "created_user": "init system",
                        }
                    )
                )
                db.add(
                    Menu(
                        **{
                            "text": "System",
                            "segment": "system",
                            "href": "#",
                            "icon": "fas fa-cogs",
                            "icon_color": "",
                            "sort": 2,
                            "menutype_id": 1,
                            "parent_id": 0,
                            "created_user": "init system",
                        }
                    )
                )
                db.add(
                    Menu(
                        **{
                            "text": "Akun",
                            "segment": "users",
                            "href": "/page/sys/users/",
                            "icon_color": "",
                            "icon": "fas fa-house-user",
                            "sort": 1,
                            "menutype_id": 1,
                            "parent_id": 2,
                            "created_user": "init system",
                        }
                    )
                )
                db.add(
                    Menu(
                        **{
                            "text": "Menu",
                            "segment": "menu",
                            "href": "/page/sys/menu/",
                            "icon_color": "",
                            "icon": "fas fa-list-alt",
                            "sort": 2,
                            "menutype_id": 1,
                            "parent_id": 2,
                            "created_user": "init system",
                        }
                    )
                )
                db.add(
                    Menu(
                        **{
                            "text": "Scope",
                            "segment": "scope",
                            "href": "/page/sys/scopes/",
                            "icon": "fas fa-map-marker-alt",
                            "icon_color": "",
                            "sort": 3,
                            "menutype_id": 1,
                            "parent_id": 2,
                            "created_user": "init system",
                        }
                    )
                )
                db.add(
                    Menu(
                        **{
                            "text": "Group",
                            "segment": "group",
                            "href": "/page/sys/groups/",
                            "icon": "fas fa-object-group",
                            "icon_color": "",
                            "sort": 4,
                            "menutype_id": 1,
                            "parent_id": 2,
                            "created_user": "init system",
                        }
                    )
                )
                db.add(
                    Menu(
                        **{
                            "text": "Gudang Link",
                            "segment": "repository",
                            "href": "/page/sys/repository/",
                            "icon": "fas fa-link",
                            "icon_color": "",
                            "sort": 5,
                            "menutype_id": 1,
                            "parent_id": 2,
                            "created_user": "init system",
                        }
                    )
                )
                db.add(
                    Menu(
                        **{
                            "text": "Setting Sistem",
                            "segment": "setting",
                            "href": "/page/sys/systemsettings/",
                            "icon": "fas fa-headset",
                            "icon_color": "",
                            "sort": 6,
                            "menutype_id": 1,
                            "parent_id": 2,
                            "created_user": "init system",
                        }
                    )
                )
                db.add(
                    Menu(
                        **{
                            "text": "Logs",
                            "segment": "logs",
                            "href": "/page/sys/logs/",
                            "icon": "fas fa-map-marked-alt",
                            "icon_color": "",
                            "sort": 7,
                            "menutype_id": 1,
                            "parent_id": 2,
                            "created_user": "init system",
                        }
                    )
                )
                db.add(
                    Menu(
                        **{
                            "text": "Session",
                            "segment": "session",
                            "href": "/page/sys/session/",
                            "icon": "fas fa-door-open",
                            "icon_color": "",
                            "sort": 8,
                            "menutype_id": 1,
                            "parent_id": 2,
                            "created_user": "init system",
                        }
                    )
                )
                db.add(
                    Menu(
                        **{
                            "text": "Documentation",
                            "segment": "documentation",
                            "href": "/page/documentation",
                            "icon": "fas fa-file-code",
                            "icon_color": "",
                            "sort": 3,
                            "menutype_id": 1,
                            "parent_id": 0,
                            "created_user": "init system",
                        }
                    )
                )
                db.commit()


async_engine = create_async_engine(DB_ENGINE)  # , echo=True)
async_session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

session_menu: Union[AsyncSession, async_scoped_session] = async_scoped_session(
    session_factory=async_session,
    scopefunc=get_session_id,
)
