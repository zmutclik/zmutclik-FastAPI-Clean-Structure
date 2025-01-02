import os
from typing import Generator

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

from . import BaseMenu as Base
from app._sys.menu.domain import Menu
from app._sys.menutype.domain import MenuType

DB_FILE = "./dbconf/_menu.db"
DB_ENGINE = "sqlite:///" + DB_FILE

engine_dbmenu = create_engine(DB_ENGINE, connect_args={"check_same_thread": False})

SessionLocalMenu = sessionmaker(autocommit=False, autoflush=False, bind=engine_dbmenu)


# Dependency
def get_dbmenu():
    db = SessionLocalMenu()
    try:
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()


if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        f.write("")

if os.path.exists(DB_FILE):
    file_stats = os.stat(DB_FILE)
    if file_stats.st_size == 0:
        Base.metadata.create_all(bind=engine_dbmenu)
