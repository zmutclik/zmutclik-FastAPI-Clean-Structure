import os
from typing import Generator

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

from . import BaseSysT as Base
from app._sys.changelog.domain import ChangeLog
from app._sys.crossorigin.domain import CrossOrigin
from app._sys.sysrepo.domain import SysRepo

DB_FILE = "./dbconf/_sys.db"
DB_ENGINE = "sqlite:///" + DB_FILE

engine_dbsys = create_engine(DB_ENGINE, connect_args={"check_same_thread": False})

SessionLocalSys = sessionmaker(autocommit=False, autoflush=False, bind=engine_dbsys)


# Dependency
def get_dbsys():
    db = SessionLocalSys()
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
        Base.metadata.create_all(bind=engine_dbsys)
