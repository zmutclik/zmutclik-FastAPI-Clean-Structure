from sqlalchemy.orm import Session
from core.config import DBCORE_FILE
from ._func import check_exits, check_sizes

def coredb_create_all():
    check_exits(DBCORE_FILE)
    if check_sizes(DBCORE_FILE):
        from datetime import datetime
        from core.config import dbcore_engine
        from ..base import BaseCore as Base
        from core.app.system.changelog.domain import ChangeLog
        from core.app.system.crossorigin.domain import CrossOrigin
        from core.app.system.sysrepo.domain import SysRepo
        from core.app.system.coresystem.domain import CoreSYSTEM

        Base.metadata.create_all(bind=dbcore_engine)
        with dbcore_engine.begin() as connection:
            with Session(bind=connection) as db:
                db.add(
                    CoreSYSTEM(
                        **{
                            "environment": "local",
                            "app_name": "FastAPI cleanStructure",
                            "app_desc": "This is a very fancy project, with auto docs for the API and everything.",
                            "app_host": "127.0.0.1",
                            "app_port": "8016",
                            "client_key": "fastapi-clean-structure_client",
                            "jwt_scret_key": "fastapi",
                            "jwt_algorithm": "HS512",
                            "cookies_key": "fastapi-clean-structure_token",
                            "cookies_exp": 30,
                            "debug": True,
                        }
                    )
                )
                db.add(
                    ChangeLog(
                        **{
                            "dateupdate": datetime.now(),
                            "version_name": "init",
                            "description": "Initial Commit",
                            "created_user": "SeMuT-CiLiK",
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
                            "created_user": "SeMuT-CiLiK",
                        }
                    )
                )

                db.add(CrossOrigin(**{"link": "http://localhost", "created_user": "SeMuT-CiLiK"}))
                db.add(CrossOrigin(**{"link": "http://127.0.0.1", "created_user": "SeMuT-CiLiK"}))
                db.add(CrossOrigin(**{"link": "http://127.0.0.1:8001", "created_user": "SeMuT-CiLiK"}))
                db.commit()
