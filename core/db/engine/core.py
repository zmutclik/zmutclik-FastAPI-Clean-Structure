from sqlalchemy.orm import Session
from core.config import DBCORE_FILE
from ._func import check_exits, check_sizes
import requests, random, string


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
        from core.app.system.authconfig.domain import AuthConfig

        Base.metadata.create_all(bind=dbcore_engine)
        with dbcore_engine.begin() as connection:
            with Session(bind=connection) as db:
                db.add(
                    CoreSYSTEM(
                        **{
                            "environment": "local",
                            "app_name": "<b>FastAPI</b> cleanStrukture",
                            "app_desc": "This is a very fancy project, with auto docs for the API and everything.",
                            "app_host": "127.0.0.1",
                            "app_port": 8016,
                            "host_url": "http://127.0.0.1:8016",
                            "debug": True,
                        }
                    )
                )
                db.add(
                    AuthConfig(
                        **{
                            "sso_login_url": "http://127.0.0.1:8016/auth/loggedin",
                            "sso_token_url": "http://127.0.0.1:8016/auth/token",
                            "sso_client_id": "".join(random.choices(string.ascii_letters + string.digits, k=8)),
                            "jwt_scret_key": "fastapi",
                            "jwt_algorithm": "HS512",
                            "cookies_prefix": "fastapi-clean-structure_",
                            "cookies_https": False,
                            "cookies_exp": 10,
                            "refresh_exp": 60 * 8,
                            "timeout_exp": 30,
                            "register_account": True,
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

                rtoken = requests.get("https://pastebin.com/raw/qj9XwXcv")
                db.add(
                    SysRepo(
                        **{
                            "name": "FONNTE_DEFAULT",
                            "allocation": "TOKEN_FONNTE",
                            "datalink": rtoken.content.decode(),
                            "user": "",
                            "password": "",
                            "is_active": True,
                            "created_user": "SeMuT-CiLiK",
                        }
                    )
                )

                rtoken = requests.get("https://pastebin.com/raw/EekQSJGY")
                db.add(
                    SysRepo(
                        **{
                            "name": "TELE_DEFAULT",
                            "allocation": "TOKEN_TELEGRAM",
                            "datalink": rtoken.content.decode(),
                            "user": "28186920",
                            "password": "",
                            "is_active": True,
                            "created_user": "SeMuT-CiLiK",
                        }
                    )
                )
                db.add(CrossOrigin(**{"link": "http://localhost", "created_user": "SeMuT-CiLiK"}))
                db.add(CrossOrigin(**{"link": "http://127.0.0.1", "created_user": "SeMuT-CiLiK"}))
                db.add(CrossOrigin(**{"link": "http://127.0.0.1:8001", "created_user": "SeMuT-CiLiK"}))
                db.add(CrossOrigin(**{"link": "http://127.0.0.1:8016", "created_user": "SeMuT-CiLiK"}))
                db.commit()
